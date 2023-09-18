#program generates a NaiveBayesClassifier using a dataset of about 40000 tweets
#classifier classifies strings into two categories: negative or positive
#this model is then pickled for use in reddit-api.py

from urllib.request import DataHandler
from stringCleanup import GetAllWords, GetPostsForModel, RemoveNoise, TheWholeShebang
from nltk import FreqDist, data
from nltk.corpus import stopwords
import random
from nltk import classify
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
import pickle

batchSize = 64

f = open("twitter-datasets/twitter_training.csv", "r")

#split into positive, negative, and neutral tweets
posTweets = []
negTweets = []
neuTweets = []

stopWords = stopwords.words('english')
stopWords.append("n't")
stopWords.append("’")

for tweet in f:
    t = tweet.lower().split(',')

    if t[0] == "positive":
        posTweets.append(t[1])

    elif t[0] == "negative":
        negTweets.append(t[1])

    else:
        neuTweets.append(t[1])

f.close()

print(len(negTweets + posTweets + neuTweets))
#creating datasets
posTweetsClean, negTweetsClean, neuTweetsClean = [], [], []

for i in range(0, len(posTweets), batchSize):
    print("batch " + str(i))
    posTweetsClean += (TheWholeShebang(posTweets[i:min(i+batchSize, len(posTweets))], stopWords))

for i in range(0, len(negTweets), batchSize):
    print("batch " + str(i))
    negTweetsClean += (TheWholeShebang(negTweets[i:min(i+batchSize, len(negTweets))], stopWords))

#for i in range(0, len(negTweets), batchSize):
#    print("batch " + str(i))
#    neuTweetsClean += (TheWholeShebang(neuTweets[i:min(i+batchSize, len(neuTweets))], stopWords))


posModelPosts = GetPostsForModel(posTweetsClean)
negModelPosts = GetPostsForModel(negTweetsClean)
#neuModelPosts = GetPostsForModel(neuTweetsClean)

positiveDataset = [(postDict, "Positive") for postDict in posModelPosts]
negativeDataset = [(postDict, "Negative") for postDict in negModelPosts]
#neutralDataset = [(postDict, "Neutral") for postDict in neuModelPosts]

dataset = positiveDataset + negativeDataset #+ neutralDataset

#shuffle dataset to remove bias
random.shuffle(dataset)
trainData = dataset[:30000]
testData = dataset[30000:]


classifier = NaiveBayesClassifier.train(trainData)

print("Accuracy is:", classify.accuracy(classifier, testData))

print(classifier.show_most_informative_features(10))

f = open('classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()



