#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
import mylogger

LOGGER = mylogger.getLogger(__name__)

CK = '3rJOl1ODzm9yZy63FACdg'
CS = '5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8'
AT = '333312023-6dTniMxvwlQG8bATKNYWBXaQkftz9t4ZjRBt7BWk'
AS = 'LQ8xXBTTN8F8CHQv9oDAqsGJFeexdnFf2DFzn3EzGH2L8'

BASEURL = 'https://api.twitter.com/1.1/'


def download_image(url):
    pass


def main():
    url = BASEURL + 'search/universal.json'
    LOGGER.info(url)
    twitter = OAuth1Session(CK, CS, AT, AS)
    params = {
        'q': '#エムグラム filter:twimg',
        'modules': 'status',
        'lang': 'ja',
        'count': '100',
    }

    req = twitter.get(url, params=params)
    LOGGER.info('API Limit: {}'.format(req.headers['x-rate-limit-remaining']))

    if req.status_code != 200:
        LOGGER.warn('STATUS CODE: {}'.format(req.status_code))
        return

    print(req.text)


if __name__ == "__main__":
    main()
