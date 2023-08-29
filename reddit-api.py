CLIENT_ID = '0esxKKReU1b1saampXysbQ'
SECRET_KEY = '_YpA_7u55AdYCqUbxG6oBDjqqGDKtg'

from nltk import tokenize
import requests
from requests.api import head
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
import re, string

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

    res = requests.get('https://oauth.reddit.com/r/learnprogramming/top/?t=month&limit=1', headers=headers)

    i = 0
    posts = []
    for post in res.json()['data']['children']:
        i += 1
        title = (post['data']['title'])
        text = (post['data']['selftext'])
        posts.append(str(title + text))

    tokens = Tokenize(posts)
    normPosts = Normalize(tokens)
    cleanPosts = RemoveNoise(normPosts)


def Tokenize(posts):
    tokens = []
    for post in posts:
        tokens.append(word_tokenize(post))

    return tokens

def Normalize(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentences = []
    lemmatized_sentence = []
    for token in tokens:
        for word, tag in pos_tag(token):
            if tag.startswith('NN'):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'
            lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
        lemmatized_sentences.append(lemmatized_sentence)
    return lemmatized_sentences

def RemoveNoise(normPosts, stopWords = ()):
    cleanedPosts = []

    for post in normPosts:
        cleanPost = []
        for token in post:
            token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
            token = re.sub("(@[A-Za-z0-9_]+)","", token)
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stopWords:
            cleanPost.append(token.lower())
        cleanedPosts.append(cleanPost)
    
    return cleanedPosts



if __name__ == "__main__":
    GetHotPosts()
