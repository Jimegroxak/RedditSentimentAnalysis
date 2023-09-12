from urllib.request import DataHandler
from stringCleanup import GetAllWords, GetPostsForModel, TheWholeShebang
from nltk import FreqDist, data
from nltk.corpus import stopwords
import random
from nltk import classify
from nltk import NaiveBayesClassifier


f = open("twitter-datasets/twitter_training.csv", "r")

#split into positive, negative, and neutral tweets
posTweets = []
negTweets = []
neutralTweets = []

stopWords = stopwords.words('english')
stopWords.append("n't")
stopWords.append("’")

for tweet in f:
    t = tweet.lower().split(',')

    if t[0] == "positive":
        posTweets.append(t[1])

    elif t[0] == "negative":
        negTweets.append(t[1])
    
    elif t[0] == "neutral":
        neutralTweets.append(t[1])

f.close()

posTweetsClean = TheWholeShebang(posTweets[:2000], stopWords)
negTweetsClean = TheWholeShebang(negTweets[:2000], stopWords)

posModelPosts = GetPostsForModel(posTweetsClean)
negModelPosts = GetPostsForModel(negTweetsClean)

positiveDataset = [(postDict, "Positive") for postDict in posModelPosts]
negativeDataset = [(postDict, "Negative") for postDict in negModelPosts]

dataset = positiveDataset + negativeDataset

#shuffle dataset to remove bias
random.shuffle(dataset)
trainData = dataset[:2800]
testData = dataset[2800:]

print(trainData)


classifier = NaiveBayesClassifier.train(trainData)

print("Accuracy is:", classify.accuracy(classifier, testData))

print(classifier.show_most_informative_features(10))

