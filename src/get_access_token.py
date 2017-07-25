#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

# Twitter 検索は5秒に一回

import tweepy


CK = '3rJOl1ODzm9yZy63FACdg'
CS = '5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8'
AT = '333312023-6dTniMxvwlQG8bATKNYWBXaQkftz9t4ZjRBt7BWk'
AS = 'LQ8xXBTTN8F8CHQv9oDAqsGJFeexdnFf2DFzn3EzGH2L8'


def main():
    auth = tweepy.OAuthHandler(CK, CS)
    print('Access:', auth.get_authorization_url())
    verifier = input('Verifier:')
    auth.get_access_token(verifier)

    print('Access Token:', auth.access_token)
    print('Access Token Secret:', auth.access_token_secret)


if __name__ == "__main__":
    main()
