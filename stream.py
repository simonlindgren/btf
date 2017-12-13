import sqlite3
import tweepy
import datetime
from tweepy.auth import OAuthHandler
import json

from q import streamingquery

consumer_key = ""
consumer_secret = ""
access_secret = ""
access_token = ""

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

conn = sqlite3.connect('livetweets.db')

# Create a twitter listener
counter = []

class MyStreamListener(tweepy.StreamListener):
    conn = sqlite3.connect('livetweets.db')
    def on_data(self, data):
        data = json.loads(data)
        tweet_id = int(data['id'])
        tweet_created_at = data['created_at']
        tweet_author = data['user']['screen_name']
        author_location = data['user']['location']
        author_followers = data['user']['followers_count'] if not None else 0
        author_friends = data['user']['friends_count'] if not None else 0
        hashtags = data['entities']['hashtags']
        tweet_hashtags = []
        for hashtag in hashtags:
            tweet_hashtags.append("#" + str(hashtag['text']))
        tweet_hashtags = ",".join(tweet_hashtags)
        tweet_text = data['text']
        in_reply_to = data['in_reply_to_screen_name']
        tweet_lang = data['lang']
        conn.execute('INSERT INTO tweets (id, created_at, author, author_location, author_followers, author_friends, hashtags, tweet, in_reply_to, lang, method) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (tweet_id, tweet_created_at, tweet_author, author_location, author_followers, author_friends, tweet_hashtags, tweet_text, in_reply_to, tweet_lang, "StreamingAPI"))
        conn.commit()
        cursor = conn.cursor()
        cursor.execute("select * from tweets")
        r = cursor.fetchall()
        print("\rTweet from " + str(tweet_created_at[:-10]) + " (" + str(len(r)) +")              ", end='')

# Create a stream
twitter_stream = tweepy.Stream(auth, MyStreamListener())

starttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("Running since " + str(starttime))

# Start streaming and check for errors
while True:
    try:
        twitter_stream.filter(track=streamingquery)
    except KeyError:
        pass
    except sqlite3.IntegrityError: # skip duplicate tweet ids
        pass


conn.close()
