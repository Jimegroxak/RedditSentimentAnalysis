# RedditSentimentAnalysis
Uses natural language processing to create a NaiveBayesClassifier for identifying trends in sentiment across Reddit forum boards
The model is a Naive Bayes Classifier trained off of the dataset found in the twitter-datasets file, originally downloaded from Kaggle
Currently, the model works with 85% accuracy and is able to process Reddit posts by combining the title and text into one string

TODO:
-add code to calculate ratio of positive to negative tweets for a specific subreddit
-allow user to manually enter a subreddit name
-get the code up and running on a webpage (probably using flask)
-???
-potentially add way for user to provide feedback or label posts for further training (training is done using tweets, not Reddit posts)
