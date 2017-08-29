#!/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth
import urllib.parse
import time
import sys
import argparse

GITHUBAPI_SERVER = 'https://api.github.com'
GH_SEARCH = '/search/issues'
GH_DEFAULT_UNIT_PER_PAGE=30
USAGE='''

Examples:

$ ghstats.py --request-user=$APIUSER \\
	--request-token=$APITOKEN \\
	--user=lpabon \\
	--repos=heketi/heketi \\
	--repos=coreos/quartermaster \\
	--date-from=2016-01-01 \\
	--date-to=2017-04-01

'''

class GHStats(object):
	def __init__(self, user, repo, date_from='', date_to='',
                request_user='', request_token='', verbose=False):
		self.user = user
		self.repo = repo
		self.date_from = date_from
		self.date_to = date_to
		self.verbose = verbose
		self.request_user = request_user
		self.request_token = request_token

		if date_from != '' and date_to != '':
			self.default_q = 'created:'+date_from+'..'+date_to
		elif date_from != '' and date_to == '':
			self.default_q = 'created:>'+date_from
		elif date_from == '' and date_to != '':
			self.default_q = 'created:<'+date_to
		else:
			self.default_q = ''

		self.default_q = self.default_q+'+repo:'+repo

	def num_pages_and_url(self, r):
		if 'Link' not in r.headers:
			return 1, r.url
		else:
			o=urllib.parse.urlparse(r.links['last']['url'])
			q=urllib.parse.parse_qs(o.query)
			return int(q['page'][0]), r.links['last']['url']

	def enumerate(self, p):
		url = GITHUBAPI_SERVER+GH_SEARCH+'?'+p
		if self.verbose:
			print("--> GET(%s)" % (url))

		if self.request_user != '' and self.request_token != '':
			auth = HTTPBasicAuth(self.request_user, self.request_token)
		else:
			auth = None

		r = requests.head(url, auth=auth)
		n, last = self.num_pages_and_url(r)

		if r.headers['X-RateLimit-Remaining'] == '0':
			print ("No more requests allowed, please wait until %s for more requests" % (time.ctime(int(r.headers['X-RateLimit-Reset']))))
			sys.exit(1)

		r = requests.get(last, auth=auth)
		body = r.json()
		if 'items' in body:
			#if self.verbose:
			#	for item in body['items']:
			#		print("#%d %s" % (item['number'], item['title']))
			return (n-1)*GH_DEFAULT_UNIT_PER_PAGE+len(body['items'])
		else:
			return (n-1)*GH_DEFAULT_UNIT_PER_PAGE

	def reviewed_authored(self):
		if self.verbose:
			print("--> Reviewed Authored:")
		query = self.default_q + '+commenter:'+self.user+'+is:pr+author:'+self.user
		params = 'q='+urllib.parse.quote(query, safe='+:')
		return self.enumerate(params)

	def reviews(self):
		if self.verbose:
			print("--> Reviews:")
		query = self.default_q + '+commenter:'+self.user
		params = 'q='+urllib.parse.quote(query, safe='+:')
		return self.enumerate(params) - self.reviewed_authored()

	def author(self):
		if self.verbose:
			print("--> Author:")
		query = self.default_q + '+is:pr+author:'+self.user
		params = 'q='+urllib.parse.quote(query, safe='+:')
		return self.enumerate(params)

### MAIN ###

parser = argparse.ArgumentParser(description='GitHub Stats utility program. Shows number of reviews and authored PRs from a user per repo', usage=USAGE)
parser.add_argument('--request-user', dest="request_user", default='', help='Owner of request token')
parser.add_argument('--request-token', dest="request_token", default='', help='Api GitHub Token')
parser.add_argument('--user', default='', help='Get stats from Github for this user')
parser.add_argument('--repos', action='append', default=[], help='Use multiple times to specify multiple repos. Ex: kubernetes/kubernetes')
parser.add_argument('--date-from', dest="date_from", default='', help='Start on this date of format YYYY-MM-DD. If date-to is not provided, stats will be returned from the date provided to today')
parser.add_argument('--date-to', dest="date_to", default='', help='End on this date of format YYYY-MM-DD. If date-from is not provided, then stats will be returned from until the date provided')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Verbose')
args = parser.parse_args()

if args.user == '':
	print("Missing user")
	sys.exit(1)
if len(args.repos) == 0:
	print("Missing repos")
	sys.exit(1)


for repo in args.repos:
	x = GHStats(args.user,
		repo,
		date_from=args.date_from,
        date_to=args.date_to,
		request_user=args.request_user,
		request_token=args.request_token,
		verbose=args.verbose)
	print("%s: Reviews(%d) Author(%d)" % (repo, x.reviews(), x.author()))
