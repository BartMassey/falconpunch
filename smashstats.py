import challonge
import elo
from os import environ

username=environ.get("CHALLONGE_USERNAME", "")
api_key=environ.get("CHALLONGE_API_KEY", "")
assert username != "" and api_key != ""
challonge.set_credentials(username, api_key)

# Who the program should print out scores for
topN = ["Lyme", "Bean", "Fest", "Nook", "Couch",
        "Meero", "Ai", "Justin", "Succulent"]

class PlayerStats(object):
    def __init__(self, rank, player, rating):
        self.rank = rank
        self.player = player
        self.rating = rating

    def to_dict(self):
        return {'rank': self.rank,
                'player': self.player,
                'rating': self.rating}

def fetchdemo():
    return [PlayerStats(1, "Lyme", 1250),
            PlayerStats(2, "Bean", 1100),
            PlayerStats(3, "Chump", 1000)]

def fetch():
    ratings = dict()

    ts = challonge.tournaments.index(created_after="2015-04-03")
    for t in ts:
        if not t["started-at"]:
            continue
        tid = t["id"]
        names = dict()
        ps = challonge.participants.index(tid)
        for p in ps:
            pid = p["id"]
            pn = p["name"]
            assert pid not in names or pn == names[pid]
            names[pid] = pn
        ms = challonge.matches.index(tid)
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

            ## EXCEPTIONS FOR INCORRECT RECORDINGS
            if p1 == "Fest" and p2 == "Nook" and ss == "2-0":
                ss = "0-2"
            if p1 == "Bean" and p2 == "Nook" and ss == "0-222":
                ss = "0-2"
            if p1 == "Ai" and p2 == "Justin" and ss == "0-69":
                ss = "0-2"
            if p1 == "Meero" and p2 == "Lyme" and ss == "0-0":
                ss == "0-2"

            # print p1, p2, ss
            if not p1 or not p2 or not ss:
                continue
            if len(ss) != 3 or ss[1] != '-' or \
               not ss[0].isdigit() or not ss[2].isdigit():
                # print >> stderr, "warning: invalid score", ss, "for", \
                #    p1, "v", p2, "in", t["name"]
                continue
            s = int(ss[0]) - int(ss[2])
            if s < -3 or s > 3:
                def pin(s0):
                    global s
                    #print >> stderr, "warning: score", s, "adjusted to", s0, \
                    #    "for", p1, "v", p2, "in", t["name"]
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

    ## ONLY PRINTS OUT THOSE WHO ARE IN TOP N
    results = []
    rank = 1
    for p in sorted(ratings, key=ratings.__getitem__, reverse=True):
        if p in topN:
            results.append(PlayerStats(rank, p, ratings[p]))
            rank += 1
    return results
