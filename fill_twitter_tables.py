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
from pprint import pprint


def populate_tweet_tables (lookup_handle, num_tweets = 5):
    tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app = Flask(__name__, template_folder = tmpl_dir)
    
    DATABASEURI = "postgresql://jy2732:1833@35.196.90.148/proj1part2"
    
    # Variables that contains the user credentials to access Twitter API 
    ACCESS_TOKEN = '3524569402-hWdaeA0moXHixJqWezA9fiajLPgxDY2zQfLHyOD'
    ACCESS_SECRET = 'qzEYoPjrQd0lH4tOajCWf1WmiL0TLD99WyTbgO1JAs60O'
    CONSUMER_KEY = 'H2sXDISrVwZJIaliuHAKZnlCA'
    CONSUMER_SECRET = 'TOfMCt6xnTmh3rbeAGDsMXfxyrjSJA5vnLd8S1DFBB1yvnvJFh'

    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)


    engine = create_engine(DATABASEURI)
    conn = engine.connect()


    twitter = Twitter(auth=oauth)


    lookup_handle=lookup_handle.lower()


    twitter_user = twitter.users.show(screen_name=lookup_handle)

    sql = """
            INSERT INTO twitter_user (handle,created_at,follower_count,location,url,profile_image)
            SELECT '%s', 
                    TO_DATE('%s','Dy Mon DD HH24:MI:SS \"XXXXX\" YYYY'),
                    %s,
                    '%s',
                    '%s',
                    '%s'
            WHERE NOT EXISTS (
                SELECT 1 FROM twitter_user WHERE handle='%s'
            );
    """ % (lookup_handle,
            twitter_user["created_at"],
            str(twitter_user["followers_count"]),
            twitter_user["location"],
            twitter_user["url"],
            twitter_user["profile_image_url"],
            lookup_handle)
    """
    conn.execute("INSERT INTO twitter_user (handle,created_at,follower_count,location,url,profile_image) VALUES \
        ('" + lookup_handle + "', TO_DATE('" + twitter_user["created_at"] + "','Dy Mon DD HH24:MI:SS \"XXXXX\" YYYY')," + \
        str(twitter_user["followers_count"]) + ",'" + twitter_user["location"] + "', '" + twitter_user["url"] + \
        "', '" + twitter_user["profile_image_url"] + "');")
    """
    conn.execute(sql)

    tweet_set = twitter.statuses.user_timeline(screen_name=lookup_handle, count = num_tweets)

    for oneTweet in tweet_set:
        tweet_id = oneTweet["id_str"]
        created_at = oneTweet["created_at"]
        retweet_count = oneTweet["retweet_count"]
        reply_count = 0 # currently can't look up
        handle = lookup_handle

        sql = """
                INSERT INTO tweet (tweet_id,created_at,retweet_count,reply_count,handle)
                SELECT '%s',
                        TO_DATE('%s','Dy Mon DD HH24:MI:SS \"XXXXX\" YYYY'),
                        %s,
                        %s,
                        '%s'
                WHERE NOT EXISTS (
                    SELECT 1 FROM tweet WHERE tweet_id='%s'
                );
        """ % (tweet_id,
                created_at,
                str(retweet_count),
                str(reply_count),
                handle,
                tweet_id)
        conn.execute(sql)
        """
        conn.execute("INSERT INTO tweet (tweet_id,created_at,retweet_count,reply_count,handle) VALUES\
            ('" + tweet_id + "',TO_DATE('" + created_at + "','Dy Mon DD HH24:MI:SS \"XXXXX\" YYYY')," + str(retweet_count) \
            + "," + str(reply_count) + ",'" + handle + "');")
        """




        tweet_text = ''.join(c for c in oneTweet["text"] if c not in '\'\";():%')
        wordFreq = Counter()
        hashtags = Counter()
        for oneWord in tweet_text.split():
            if "http" not in oneWord and "#" not in oneWord:
                wordFreq[oneWord] += 1
            if "http" not in oneWord and oneWord[0] == "#":
                hashtags[oneWord] += 1

        for eachWord in wordFreq:
            wordF = wordFreq[eachWord]

            sql = """
                INSERT INTO twitter_word (word,frequency,tweet_id)
                SELECT '%s',
                        %s,
                        '%s'
                WHERE NOT EXISTS (
                    SELECT 1 FROM twitter_word
                    WHERE word='%s' AND tweet_id='%s'
                );
            """ % (eachWord,str(wordF),tweet_id,eachWord,tweet_id)
            conn.execute(sql)
            """
            conn.execute("INSERT INTO twitter_word (word,frequency,tweet_id) VALUES\
                ('" + eachWord + "'," + str(wordF) + ",'" + tweet_id + "');")
            """

        for hashtag in hashtags:
            sql = """
                    INSERT INTO hashtag (name,total_twitter_freq)
                    SELECT '%s',0
                    WHERE NOT EXISTS (
                        SELECT * FROM hashtag WHERE name='%s');
            """ % (hashtag,hashtag)
            conn.execute(sql)
            """
            conn.execute("INSERT INTO hashtag (name,total_twitter_freq) \
                SELECT '" + hashtag +"',0 WHERE NOT EXISTS (SELECT * FROM hashtag WHERE name='" + hashtag + "');") # no way to get total occurances of a hashtag from twitter API
            """

            sql = """
                    INSERT INTO hashtag_member (name,tweet_id)
                    SELECT '%s','%s'
                    WHERE NOT EXISTS (
                        SELECT 1 FROM hashtag_member
                        WHERE name='%s' AND tweet_id='%s'
                    );
            """ % (hashtag,tweet_id,hashtag,tweet_id)
            conn.execute(sql)
            """
            conn.execute("INSERT INTO hashtag_member (name,tweet_id) VALUES\
                ('" + hashtag + "','" + tweet_id + "');")
            """
    conn.close()

if __name__ == "__main__":
    handles = ["HillaryClinton", "realDonaldTrump", "GovGaryJohnson"]
    for handle in handles:
        populate_tweet_tables(handle, 10)
