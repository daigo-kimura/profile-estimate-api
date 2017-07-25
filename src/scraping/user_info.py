#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import time
import urllib
from bs4 import BeautifulSoup


BASE_URL = 'https://api.twitter.com/1.1/'


def get_soup(url, sleep=1.0):
    time.sleep(sleep)
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/39.0.2171.95 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read()
    soup = BeautifulSoup(html, "html5lib")
    return soup


def main():
    url = 'users/lookup.json'
    # ?user_id=1528352858%2C2905085521&include_entities=true'


if __name__ == "__main__":
    main()
