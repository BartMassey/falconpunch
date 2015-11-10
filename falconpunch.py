#!/usr/bin/python3
# Copyright (c) 2015 Benjamin and Barton Massey
# [This program is licensed under the GPL version 3 or later.]
# Please see the file COPYING in the source
# distribution of this software for license terms.

# FalconPunch: Lakeridge Smash Club Ratings API

# Uses http://challonge.com for tournament info.

# Uses http://falconframework.org WSGI framework with Gunicorn
# to provide web API.

import falcon
import json
 
class QuoteResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'quote': 'I\'ve always been more interested in the future than in the past.',
            'author': 'Grace Hopper'
        }

        resp.body = json.dumps(quote)
 
api = falcon.API()
api.add_route('/quote', QuoteResource())
