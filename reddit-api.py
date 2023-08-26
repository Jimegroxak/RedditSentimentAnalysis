CLIENT_ID = '0esxKKReU1b1saampXysbQ'
SECRET_KEY = '_YpA_7u55AdYCqUbxG6oBDjqqGDKtg'

import requests
from requests.api import head

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

with open('pw.txt', 'r') as f:
    pw = f.read()

data = {'grant_type': 'password',
        'username': 'jimegroxak',
        'password': pw}
headers = {'User-Agent': 'MyAPI/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']
headers['Authorization'] = f'bearer {TOKEN}'

res = requests.get('https://oauth.reddit.com/r/gaming/top/?t=month', headers=headers)

for post in res.json()['data']['children']:

    print(post['data']['title'])
    print(post['data']['selftext'])

