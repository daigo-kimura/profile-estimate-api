#! /usr/local/bin/python3
# -*- coding: utf-8 -*-


import time
import re
import urllib
from bs4 import BeautifulSoup


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
    query = '男性'

    page = 1
    query = urllib.parse.quote(query)

    # 無限ループは良くない
    while True:
        url = 'http://twpf.jp/search/profile\
?page={}&sort=modified&direction=desc\
&target=personal_tag&keyword={}'.format(page, query)
        soup = get_soup(url)
        results = soup.find_all('div', class_='profile clearfix')

        for result in results:
            user_id = re.match(r'@[^ ]+',
                               result.find('div', class_='name').get_text())
            if user_id is not None:
                user_id = user_id.group(0)
                print(user_id)
        page += 1


if __name__ == "__main__":
    main()
