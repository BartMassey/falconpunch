#!/usr/bin/python2
# Copyright (c) 2015 Benjamin and Barton Massey
# [This program is licensed under the GPL version 3 or later.]
# Please see the file COPYING in the source
# distribution of this software for license terms.

# Query Challonge and print each tournament id / date / title

from challonge import *
from os import environ

username=environ.get("CHALLONGE_USERNAME", "")
api_key=environ.get("CHALLONGE_API_KEY", "")
assert username != "" and api_key != ""
    
set_credentials(username, api_key)

ts = tournaments.index(created_after="2015-04-03")
for t in ts:
    start = t["started-at"]
    if not start:
        continue
    print "%s,\"%s\",\"%s\"" % (t["id"], start, t["name"])
