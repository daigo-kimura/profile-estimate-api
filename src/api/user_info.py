#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import json
import re
import mytwitter


def main():
    file_name = 'woman_account_list'
    screen_names = []
    group_by = 8
    with open(file_name, 'r') as f:
        screen_names = f.read().split("\n")
        while screen_names.count("") > 0:
            screen_names.remove("")

    screen_names = [re.sub(r"^@", "", n) for n in screen_names]
    # print(screen_names)
    for i in range(0, len(screen_names), group_by):
        params = {
            'screen_name': ','.join(screen_names[i:i + group_by]),
            'include_entities': 'true',
        }
        req = mytwitter.get_instance('users/lookup.json', params)
        print(req.text)
        result = json.loads(req.text)

        for r in result:
            file_name = 'data/female/{}.json'.format(r['screen_name'])
            with open(file_name, 'w+') as f:
                f.write(json.dumps(r, indent=4))


if __name__ == "__main__":
    main()
