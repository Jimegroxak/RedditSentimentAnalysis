#Set of functions to assist in cleaning strings for use with the neural network
import nltk
from nltk import tokenize
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import FreqDist
import re, string


def Tokenize(posts):
    tokens = []
    for post in posts:
        tokens.append(word_tokenize(post))

    return tokens

def Normalize(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentences = []
    for token in tokens:
        lemmatized_sentence = []
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

def GetAllWords(cleanPosts):
    for tokens in cleanPosts:
        for token in tokens:
            yield token

def TheWholeShebang(strings, stopWords=()):
    tokens = Tokenize(strings)
    lemSent = Normalize(tokens)
    cleanStrings = RemoveNoise(lemSent, stopWords)
    return cleanStrings

#function to be used on a list of clean tokenized strings
def GetPostsForModel(cleanPosts):
    for postToken in cleanPosts:
        yield dict([token, True] for token in postToken)