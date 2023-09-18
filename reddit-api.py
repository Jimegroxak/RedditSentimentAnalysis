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

    subreddit = input("Enter desired subreddit: r/")
    url = 'https://oauth.reddit.com/r/' + subreddit + '/top/?t=month'

    res = requests.get(url, headers=headers)
    print(res.json()['data']['after'])

    posts = []
    for post in res.json()['data']['children']:
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
    f.close()

    pos, neg = 0, 0

    for post in cleanPosts:
        res = classifier.classify(dict([token, True] for token in post))
        if res == 'Positive':
            pos += 1
        else:
            neg += 1

    print("positive/negative ratio: " + str(pos) + '/' + str(neg))

if __name__ == "__main__":
    GetHotPosts()
