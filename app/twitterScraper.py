# Need to fix and clean up
# - Last 100 Tweets
# - return text and sentiment

import tweepy
from textblob import TextBlob
import re
import config
import string

auth = tweepy.OAuthHandler(config.api_key, config.api_secret_key)
auth.set_access_token(config.access_token, config.access_secret_token)

api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        """
        Returns the full text of a searched tweet via the Twitter Streamer
        """
        if hasattr(status, "retweeted_status"):
            try:
                text = status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                text = status.retweeted_status.text

        else:
            try:
                text = status.extended_tweet["full_text"]
            except AttributeError:
                text = status.text

        self.get_details(status)

        return text

    def get_details(self, status):
        """
        Returns the tweet author, handle, date/time of the tweet (for display purposes)
        """
        return status.user.name, status.user.screen_name, status.user.location, status.created_at


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

    return text


def sentiment_analysis(tweet):
    """
    Returns sentiment analysis data on text
    """
    analysis = TextBlob(tweet)
    print(analysis.sentiment[0])
    return analysis.sentiment[0]


def last_100_tweets(search):
    """
    Returns last 100 tweets on searched item
    """
    return api.search(search, count=100, lang='en')


if __name__ == '__main__':
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    stream = myStream.filter(track=['nike'], languages=["en"])
