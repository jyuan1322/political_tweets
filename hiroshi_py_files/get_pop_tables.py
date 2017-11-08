try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from collections import Counter

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response



def populate_tweet_tables (lookup_handle, num_tweets = 5):
    tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app = Flask(__name__, template_folder = tmpl_dir)
    
    DATABASEURI = "postgresql://hf2326:2307@35.196.90.148/proj1part2"
    
    # Variables that contains the user credentials to access Twitter API 
    ACCESS_TOKEN = '3524569402-hWdaeA0moXHixJqWezA9fiajLPgxDY2zQfLHyOD'
    ACCESS_SECRET = 'qzEYoPjrQd0lH4tOajCWf1WmiL0TLD99WyTbgO1JAs60O'
    CONSUMER_KEY = 'H2sXDISrVwZJIaliuHAKZnlCA'
    CONSUMER_SECRET = 'TOfMCt6xnTmh3rbeAGDsMXfxyrjSJA5vnLd8S1DFBB1yvnvJFh'

    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)


    engine = create_engine(DATABASEURI)
    conn = engine.connect()


    twitter = Twitter(auth=oauth)

    twitter_user = twitter.users.show(screen_name=lookup_handle)

    conn.execute("INSERT INTO twitter_user (handle,created_at,follower_count,location,url,profile_image) VALUES \
        ('" + lookup_handle + "', TO_DATE('" + twitter_user["created_at"] + "','Dy Mon DD HH24:MI:SS \"XXXXX\" YYYY')," + \
        str(twitter_user["followers_count"]) + ",'" + twitter_user["location"] + "', '" + twitter_user["url"] + \
        "', '" + twitter_user["profile_image_url"] + "');")


    tweet_set = twitter.statuses.user_timeline(screen_name=lookup_handle, count = num_tweets)

    for oneTweet in tweet_set:
        tweet_id = oneTweet["id_str"]
        created_at = oneTweet["created_at"]
        retweet_count = oneTweet["retweet_count"]
        reply_count = 0 # currently can't look up
        handle = lookup_handle

        conn.execute("INSERT INTO tweet (tweet_id,created_at,retweet_count,reply_count,handle) VALUES\
            ('" + tweet_id + "',TO_DATE('" + created_at + "','Dy Mon DD HH24:MI:SS \"XXXXX\" YYYY')," + str(retweet_count) \
            + "," + str(reply_count) + ",'" + handle + "');")

#        tweet_text = oneTweet["text"]
        tweet_text = ''.join(c for c in oneTweet["text"] if c not in '\'\";():')
        wordFreq = Counter()
        hashtags = Counter()
        for oneWord in tweet_text.split():
            if "http" not in oneWord and "#" not in oneWord:
                wordFreq[oneWord] += 1
            if "http" not in oneWord and oneWord[0] == "#":
                hashtags[oneWord] += 1

        for eachWord in wordFreq:
            wordF = wordFreq[eachWord]
            conn.execute("INSERT INTO twitter_word (word,frequency,tweet_id) VALUES\
                ('" + eachWord + "'," + str(wordF) + ",'" + tweet_id + "');")

        for hashtag in hashtags:
#            conn.execute("INSERT INTO hashtag (name,total_twitter_freq) VALUES\
#                ('" + hashtag +"',0) WHERE NOT EXISTS (SELECT * FROM hashtag WHERE name='" + hashtag + "');") # no way to get total occurances of a hashtag from twitter API
#            conn.execute("INSERT INTO hashtag (name,total_twitter_freq) VALUES\
#                ('" + hashtag + "',0)")            
            conn.execute("INSERT INTO hashtag (name,total_twitter_freq) \
                SELECT '" + hashtag +"',0 WHERE NOT EXISTS (SELECT * FROM hashtag WHERE name='" + hashtag + "');") # no way to get total occurances of a hashtag from twitter API

            conn.execute("INSERT INTO hashtag_member (name,tweet_id) VALUES\
                ('" + hashtag + "','" + tweet_id + "');")

if __name__ == "__main__":
    handles = ["HillaryClinton", "realDonaldTrump", "GovGaryJohnson"]
    for handle in handles:
        populate_tweet_tables(handle, 10)


