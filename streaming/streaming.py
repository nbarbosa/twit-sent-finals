from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from sklearn.externals import joblib
from selectors import ItemSelector
from tokenizers import tweet_tokenize
import pandas as pd
from pymongo import MongoClient
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key=""
consumer_secret=""

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token=""
access_token_secret=""

track_terms = ['finals']
print(os.environ['MONGO_URL'])
mongo_client = MongoClient(os.environ['MONGO_URL'])
db = mongo_client.get_default_database()

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        json_load = json.loads(data)
        try:
          
          # if any(bigram in json_load['text'].lower() for bigram in track_terms):
              sentiment_proba = clf.predict_proba(pd.DataFrame([{'text': json_load['text']}]))[0]
              max_proba = max(sentiment_proba)
              if max_proba >= 0.75:
                sentiment = 'positive'
                if sentiment_proba[0] == max_proba:
                  sentiment = 'negative'
                print(json_load['text'] + ' - ' + sentiment + ' - ' + json_load['created_at'])
                db.tweets.insert_one({
                  'ts_created': time.time(),
                  'tweet': json_load,
                  'sentiment': sentiment
                  })
                db.sentiment_counts.update_one({}, { '$inc': {sentiment: 1} }, upsert=True)
        except KeyError:
          return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    print("setting stream up")
    clf = joblib.load('sent_model.pkl')
    print("loaded model")
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(languages=['en'],track=track_terms)