# Need to fix and clean up
# - Twitter streamer
# - Last 100 Tweets
# - return text and sentiment

import tweepy
from textblob import TextBlob
import preprocessor as p
import re
import matplotlib.pyplot as plt
import numpy as np
import config

auth = tweepy.OAuthHandler(config.api_key, config.api_secret_key)
auth.set_access_token(config.access_token, config.access_secret_token)

api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        self.clean_tweet(status.text)
        self.sentiment(status.text)

    def clean_tweet(self, tweet):
        tweet = re.sub(r'http\S+', '', tweet)
        p.clean(tweet)
        strip = [':', '.', '-', '+', '[', ']', '{', '}', '!', '@', '^', '%', '&', '*', '(', ')', '...']
        for i in strip:
            tweet = tweet.replace(i, '')
        print(tweet)

    def sentiment(self, tweet):
        analysis = TextBlob(tweet)
        print(analysis.sentiment[0])
        return analysis.sentiment[0]


def last_100_tweets(search):
    #print(api.search(search, count=10, lang='en'))
    return api.search(search, count=100, lang='en')


def setup(text):
    print(last_100_tweets(text))

    #myStreamListener = MyStreamListener()
    #myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    #stream = myStream.filter(track=[text])


print(setup('nike'))
