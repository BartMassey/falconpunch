#!/usr/bin/python3
# Copyright (c) 2015 Benjamin and Barton Massey
# [This program is licensed under the GPL version 3 or later.]
# Please see the file COPYING in the source
# distribution of this software for license terms.

# Query Challonge and print all match scores for all tournaments.

from challonge import *
from os import environ
from sys import stderr
import elo

ratings = dict()

username=environ.get("CHALLONGE_USERNAME", "")
api_key=environ.get("CHALLONGE_API_KEY", "")
assert username != "" and api_key != ""
    
set_credentials(username, api_key)

ts = tournaments.index(created_after="2015-04-03")
for t in ts:
    if not t["started-at"]:
        continue
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
        if len(ss) != 3 or ss[1] != '-' or \
           not ss[0].isdigit() or not ss[2].isdigit():
            print >> stderr, "warning: invalid score", ss, "for", \
                p1, "v", p2, "in", t["name"]
            continue
        s = int(ss[0]) - int(ss[2])
        if s < -3 or s > 3:
            def pin(s0):
                global s
                print >> stderr, "warning: score", s, "adjusted to", s0, \
                    "for", p1, "v", p2, "in", t["name"]
                s = s0
            if s < -3:
                pin(-3)
            if s > 3:
                pin(3)
        if p1 not in ratings:
            ratings[p1] = 1000
        if p2 not in ratings:
            ratings[p2] = 1000
        p1r = ratings[p1]
        p2r = ratings[p2]
        sn = (s + 3.0) / 6.0
        ratings[p1] = elo.update(p1r, p2r, sn)
        ratings[p2] = elo.update(p2r, p1r, 1.0 - sn)
        def d(p, pr):
            return p + ":" + str(pr) + "->" + str(ratings[p])
        # print >> stderr, "update", sn, d(p1, p1r), d(p2, p2r)

for p in sorted(ratings, key=ratings.__getitem__, reverse=True):
    print p, ratings[p]
