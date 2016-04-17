import json

import falcon
import requests

import smashstats

class Smashers(object):
    def on_get(self, req, resp):
        stats = smashstats.fetch()
        for i in range(len(stats)):
            stats[i] = stats[i].to_dict()
        resp.body = json.dumps(stats)
        resp.status = falcon.HTTP_200

smashers = Smashers()

app = falcon.API()
app.add_route('/smashers', smashers)
