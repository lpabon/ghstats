# ghstats
GitHub Stats utility program. Shows number of reviews and authored PRs from a user per repo

```
$ ./ghstats.py -h
usage: 

Examples:

$ ghstats.py --request-user=$APIUSER \
	--request-token=$APITOKEN \
	--user=lpabon \
	--repos=heketi/heketi \
	--repos=coreos/quartermaster \
	--date-from=2016-01-01 \
	--date-to=2017-04-01

GitHub Stats utility program. Shows number of reviews and authored PRs from a
user per repo

optional arguments:
  -h, --help            show this help message and exit
  --request-user REQUEST_USER
                        Owner of request token
  --request-token REQUEST_TOKEN
                        Api GitHub Token
  --user USER           Get stats from Github for this user
  --repos REPOS         Use multiple times to specify multiple repos. Ex:
                        kubernetes/kubernetes
  --date-from DATE_FROM
                        Start on this date of format YYYY-MM-DD. If date-to is
                        not provided, stats will be returned from the date
                        provided to today
  --date-to DATE_TO     End on this date of format YYYY-MM-DD. If date-from is
                        not provided, then stats will be returned from until
                        the date provided
  -v, --verbose         Verbose

$ ./ghstats.py --request-user=$APIUSER \
	--request-token=$APITOKEN \
	--user=lpabon \
	--repos=heketi/heketi \
	--repos=coreos/quartermaster \
	--date-from=2016-01-01 \
	--date-to=2017-04-01
lpabon heketi/heketi: Reviews(186) Author(132)
lpabon coreos/quartermaster: Reviews(11) Author(45)
Total: Reviews(197) Author(177)
```

