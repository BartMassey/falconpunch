#!/usr/bin/python3
# Copyright (c) 2015 Benjamin and Barton Massey
# [This program is licensed under the GPL version 3 or later.]
# Please see the file COPYING in the source
# distribution of this software for license terms.

# Query Challonge and print all match scores for all tournaments.

from challonge import *
from os import environ
import elo

ratings = dict()

username=environ.get("CHALLONGE_USERNAME", "")
api_key=environ.get("CHALLONGE_API_KEY", "")
assert username != "" and api_key != ""
    
set_credentials(username, api_key)

ts = tournaments.index()
for t in ts:
    tid = t["id"]
    names = dict()
    ps = participants.index(tid)
    for p in ps:
        pid = p["id"]
        pn = p["name"]
        assert pid not in names or pn == names[pid]
        names[pid] = pn
    ms = matches.index(tid)
    for m in ms:
        id1 = m["player1-id"]
        if not id1:
            continue
        p1 = names[id1]
        id2 = m["player2-id"]
        if not id2:
            continue
        p2 = names[id2]
        ss = m["scores-csv"]
        if not p1 or not p2 or not ss:
            continue
        assert ss[1] == '-' and ss[0].isdigit() and ss[2].isdigit()
        s = int(ss[0]) - int(ss[2])
        if p1 not in ratings:
            ratings[p1] = 1000
        if p2 not in ratings:
            ratings[p2] = 1000
        ratings[p1] = elo.update(ratings[p1], ratings[p2], (s + 3) / 6)
        ratings[p2] = elo.update(ratings[p2], ratings[p1], ((3 - s) + 3) / 6)
for p in ratings:
    print p, round(ratings[p])