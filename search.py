import sqlite3
import tweepy
import datetime
from tweepy.auth import OAuthHandler
import json

from q import searchquery


consumer_key = ""
consumer_secret = ""
access_secret = ""
access_token = ""

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

conn = sqlite3.connect('histtweets.db')

start = str(datetime.date.today() - datetime.timedelta(days=3))

c = tweepy.Cursor(api.search,
                  q=searchquery,
                  since = start,
                  wait_on_rate_limit = True,
                  wait_on_rate_limit_notify=True).items()



starttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("Searching backwards since " + str(starttime))

while True:
    try:
        tweet = c.next()
        json_tweet = tweet._json

        try:
            tweet_id = json_tweet['id_str']
            tweet_created_at = json_tweet['created_at']
            tweet_author = json_tweet['user']['screen_name']
            author_location = json_tweet['user']['location']
            author_followers = json_tweet['user']['followers_count'] if not None else 0
            author_friends = json_tweet['user']['friends_count'] if not None else 0
            hashtags = json_tweet['entities']['hashtags']
            tweet_hashtags = []
            for hashtag in hashtags:
                tweet_hashtags.append("#" + str(hashtag['text']))
            tweet_hashtags = ",".join(tweet_hashtags)
            tweet_text = json_tweet['text']
            to_whom = json_tweet['in_reply_to_screen_name']
            tweet_lang = json_tweet['lang']
            conn.execute('INSERT INTO tweets (id, created_at, author, author_location, author_followers, author_friends, hashtags, tweet, in_reply_to, lang, method) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (tweet_id, tweet_created_at, tweet_author, author_location, author_followers, author_friends, tweet_hashtags, tweet_text, to_whom, tweet_lang, "StreamingAPI"))
            conn.commit()
            cursor = conn.cursor()
            cursor.execute("select * from tweets")
            r = cursor.fetchall()
            print("\rTweet from " + str(tweet.created_at) + " (" + str(len(r)) +")              ", end='')
        except KeyError:
            print("Key Error")

        except sqlite3.IntegrityError:
            print("\rAlready in database, continuing...", end="")

    except IOError:
        time.sleep(60*5)
        continue
    except StopIteration:
        break

print("Done!")
conn.close()
