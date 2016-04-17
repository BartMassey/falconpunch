#!/bin/sh
cd /home/fpunch/falconpunch
case "$1" in
    start)  python2 ./falconpunch.py ;;
    stop)   PID=`cat falconpunch.pid` &&
	    kill $PID ;;
esac
