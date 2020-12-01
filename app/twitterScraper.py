import tweepy
from textblob import TextBlob
import preprocessor as p
import re
import matplotlib.pyplot as plt
import numpy as np
import config

auth = tweepy.OAuthHandler(config.api_key, config.api_secret_key)
auth.set_access_token(config.access_token, config.access_token_secret)

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



def setup(text):
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    stream = myStream.filter(track=[text])


print(setup('nike'))