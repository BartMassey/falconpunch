#!/bin/sh
cd /home/fpunch/falconpunch
case "$1" in
    start)
	. ./challonge-api.sh
	gunicorn -D -u fpunch -p ./falconpunch.pid -b 0.0.0.0:5256 \
	  --log-file=./falconpunch.log
	  falconpunch:app
	;;
    stop)
	PID=`cat falconpunch.pid` &&
	kill $PID
	;;
esac
