#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import math
import json
import twitter_api

MEAN = 0.5
VAR = 0.3


def calc_mote(screenname):
    params = {
        "screen_name": screenname,
        "count": 200,
        "include_user_entities": True,
    }
    req = twitter_api.get_instance('followers/list', params=params)
    followers = json.loads(req.text)
    clf = 'A'

    for f in followers:
        clf.predict()
        rate = 0.5

    return ((rate - MEAN) / math.sqrt(VAR)) * 0.1 + 0.5


def main():
    pass
