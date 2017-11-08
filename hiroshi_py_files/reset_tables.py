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




def reset_tables():

    tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app = Flask(__name__, template_folder = tmpl_dir)
    
    DATABASEURI = "postgresql://hf2326:2307@35.196.90.148/proj1part2"

    engine = create_engine(DATABASEURI)
    conn = engine.connect()
    
    conn.execute("DROP TABLE IF EXISTS WIKI_WORD_AGGREGATE;")
    conn.execute("DROP TABLE IF EXISTS WIKIPEDIA_PAGE;")
    conn.execute("DROP TABLE IF EXISTS HASHTAG_MEMBER;")
    conn.execute("DROP TABLE IF EXISTS HASHTAG;")
    conn.execute("DROP TABLE IF EXISTS TWITTER_WORD;")
    conn.execute("DROP TABLE IF EXISTS TWEET;")
    conn.execute("DROP TABLE IF EXISTS TWITTER_USER;")
    conn.execute("DROP TABLE IF EXISTS POLITICAL_PARTY;")
    conn.execute("CREATE TABLE TWITTER_USER\
    (handle VARCHAR(255),\
     created_at DATE NOT NULL,\
     follower_count INT DEFAULT 0,\
     location VARCHAR(255),\
     url VARCHAR(255) NOT NULL,\
     profile_image VARCHAR(255),\
     PRIMARY KEY (handle),\
     UNIQUE (url),\
     CHECK (follower_count >= 0));")

    conn.execute("CREATE TABLE TWEET\
    (tweet_id VARCHAR(255),\
     created_at DATE NOT NULL,\
     retweet_count INT DEFAULT 0,\
     reply_count INT DEFAULT 0,\
     handle VARCHAR(255),\
     PRIMARY KEY (tweet_id),\
     CHECK (retweet_count >= 0),\
     CHECK (reply_count >= 0),\
     FOREIGN KEY (handle) REFERENCES TWITTER_USER\
         ON DELETE CASCADE);")
    
    conn.execute("CREATE TABLE TWITTER_WORD\
    (word VARCHAR(255),\
     frequency INT NOT NULL,\
     tweet_id VARCHAR(255),\
     PRIMARY KEY (tweet_id, word),\
     FOREIGN KEY (tweet_id) REFERENCES TWEET\
         ON DELETE CASCADE);")
    
    conn.execute("CREATE TABLE HASHTAG\
    (name VARCHAR(255),\
     total_twitter_freq INT NOT NULL,\
     PRIMARY KEY (name));")
    
    conn.execute("CREATE TABLE HASHTAG_MEMBER\
    (name VARCHAR(255),\
     tweet_id VARCHAR(255),\
     PRIMARY KEY (name, tweet_id),\
     FOREIGN KEY (name) REFERENCES HASHTAG\
         ON DELETE CASCADE,\
     FOREIGN KEY (tweet_id) REFERENCES TWEET\
         ON DELETE CASCADE);")
    
    conn.execute("CREATE TABLE POLITICAL_PARTY\
    (name VARCHAR(255),\
     agg_sentiment_score FLOAT(8) DEFAULT 0,\
     PRIMARY KEY (name));")
    
    conn.execute("CREATE TABLE WIKIPEDIA_PAGE\
    (wiki_page_name VARCHAR(255),\
     name VARCHAR(255) NOT NULL,\
     date_of_birth DATE,\
     sentiment_score FLOAT(8) DEFAULT 0,\
     summary_text VARCHAR NOT NULL,\
     political_party VARCHAR(255) NOT NULL,\
     handle VARCHAR(255) NOT NULL,\
     PRIMARY KEY (wiki_page_name),\
     UNIQUE (handle),\
     UNIQUE (name),\
     FOREIGN KEY (handle) REFERENCES TWITTER_USER\
         ON DELETE CASCADE,\
     FOREIGN KEY (political_party) REFERENCES POLITICAL_PARTY\
         ON DELETE SET NULL);")
    
    conn.execute("CREATE TABLE WIKI_WORD_AGGREGATE\
    (word VARCHAR(255),\
     frequency INT NOT NULL,\
     wiki_page_name VARCHAR(255),\
     PRIMARY KEY (wiki_page_name, word),\
     FOREIGN KEY (wiki_page_name) REFERENCES WIKIPEDIA_PAGE\
         ON DELETE CASCADE);")


if __name__ == "__main__":
    reset_tables()

