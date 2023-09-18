CLIENT_ID = '0esxKKReU1b1saampXysbQ'
SECRET_KEY = '_YpA_7u55AdYCqUbxG6oBDjqqGDKtg'

from nltk import tokenize
import requests
from requests.api import head
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import FreqDist
import re, string
from stringCleanup import *
import pickle

def GetHotPosts():
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

    res = requests.get('https://oauth.reddit.com/r/gaming/top/?t=month&limit=25', headers=headers)

    i = 0
    posts = []
    for post in res.json()['data']['children']:
        i += 1
        title = (post['data']['title'])
        text = (post['data']['selftext'])
        posts.append(str(title + text))

    stopWords = stopwords.words('english')
    stopWords.append("n't")
    stopWords.append("’")


    cleanPosts = TheWholeShebang(posts, stopWords)
    #import classifier and classify the posts

    f = open('classifier.pickle', 'rb')
    classifier = pickle.load(f)
    #f.close()

    i = 0
    for post in cleanPosts:
        print(posts[i])
        print(classifier.classify(dict([token, True] for token in post)))
        i += 1

if __name__ == "__main__":
    GetHotPosts()
