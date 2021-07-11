# TODO: Need to fix and clean up Last 100 Tweets
# TODO: Return text and sentiment
# TODO: Still need to fix NLP -> does not recognise 'fire' is positive

import tweepy
from textblob import TextBlob
import re
from config import Twitter
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def authentication():
    '''
    Authenticate Twitter credentials
    '''
    auth = tweepy.OAuthHandler(Twitter.API_KEY, Twitter.API_SECRET_KEY)
    auth.set_access_token(Twitter.ACCESS_TOKEN, Twitter.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    return api


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        """
        Returns the full text of a searched tweet via the Twitter Streamer including tweet author, handle,
        date/time of the tweet
        """
        if hasattr(status, "retweeted_status"):
            # Get full text of retweeted Tweet
            try:
                text = status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                text = status.retweeted_status.text

        else:
            # Get text of normal Tweet
            try:
                text = status.extended_tweet["full_text"]
            except AttributeError:
                text = status.text

        message = preprocess_tweet(text)
        sentiment_analysis(message)

        return text, status.user.name, status.user.screen_name, status.user.location, status.created_at


def preprocess_tweet(tweet):
    """
    Prepares the text in a tweet for sentiment analysis. Returns tokenized and cleaned words
    """
    # Remove Links
    text = re.sub(r'http\S+', '', tweet)

    # Remove Emojis
    regrex_pattern = re.compile(pattern="["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)
    text = regrex_pattern.sub(r'', text)

    # Remove punctuation and numbers
    text = "".join([char for char in text if char not in string.punctuation])
    text = re.sub("[0-9]+", '', text)

    # Remove new lines
    text = text.replace('\n', ' ')

    return text


def sentiment_analysis(tweet):
    """
    Returns sentiment analysis data on text
    """
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(tweet)
    for k in sorted(ss):
        print('{0}: {1}, '.format(k, ss[k]), end='')
    return


def last_100_tweets(api, search):
    """
    Returns last 100 tweets on searched item
    """
    tweets = api.search(search, count=100, lang='en', tweet_mode='extended')
    return tweets

