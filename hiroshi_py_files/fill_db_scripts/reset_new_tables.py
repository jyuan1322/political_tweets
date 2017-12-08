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




def reset_new_tables():

    tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app = Flask(__name__, template_folder = tmpl_dir)

    DATABASEURI = "postgresql://hf2326:2307@35.196.90.148/proj1part2"

    engine = create_engine(DATABASEURI)
    conn = engine.connect()


    conn.execute("DROP TYPE IF EXISTS DONATION_INFO;")
    conn.execute("DROP TABLE IF EXISTS POLITICIAN_DONATIONS;")
    conn.execute("DROP TABLE IF EXISTS POLITICIAN_NEWS;")

    conn.execute("CREATE TYPE DONATION_INFO AS\
    (recipient_name VARCHAR(255),\
    donation_amt DECIMAL(15,2),\
    donation_date DATE);")

    conn.execute("CREATE TABLE POLITICIAN_DONATIONS\
    (donate_id INT,\
    politician_handle VARCHAR(255),\
    donation DONATION_INFO NOT NULL,\
    PRIMARY KEY (donate_id),\
    FOREIGN KEY (politician_handle) REFERENCES TWITTER_USER\
        ON DELETE CASCADE);")

    conn.execute("CREATE TABLE POLITICIAN_NEWS\
    (article_id INT,\
    url VARCHAR(255) NOT NULL,\
    publisher VARCHAR(255) NOT NULL,\
    date_pub DATE NOT NULL,\
    article_title VARCHAR(255) NOT NULL,\
    article_text VARCHAR(255) NOT NULL,\
    politician_handle VARCHAR(255) NOT NULL,\
    tags VARCHAR(255)[],\
    PRIMARY KEY (article_id),\
    FOREIGN KEY (politician_handle) REFERENCES TWITTER_USER\
        ON DELETE CASCADE);")

    conn.close()

if __name__ == "__main__":
    reset_new_tables()
