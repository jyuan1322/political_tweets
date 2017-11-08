try:
    import json
except ImportError:
    import simplejson as json

import wikipedia
from collections import Counter
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

def populate_wiki_tables (lookup_name, handle, party):

    tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app = Flask(__name__, template_folder = tmpl_dir)
    
    DATABASEURI = "postgresql://hf2326:2307@35.196.90.148/proj1part2"

    engine = create_engine(DATABASEURI)
    conn = engine.connect()

    conn.execute("INSERT INTO POLITICAL_PARTY (name) \
        SELECT '" + party.lower() + "' WHERE NOT EXISTS (SELECT * FROM POLITICAL_PARTY WHERE name = '" + party + "');")


    lookup_name=lookup_name.lower()
    handle = handle.lower()

    suggestedPage = wikipedia.suggest(lookup_name)

    if suggestedPage == None:
        suggestedPage = lookup_name

    currPage = wikipedia.page(suggestedPage)
    summary_text = ''.join(c for c in wikipedia.summary(suggestedPage) if c not in '\'\";():%')

    conn.execute("INSERT INTO wikipedia_page (wiki_page_name,name,date_of_birth,sentiment_score,summary_text,political_party,handle) VALUES \
        ('" + currPage.title + "','" + suggestedPage + "', TO_DATE('1/1/2017', 'DD/MM/YYYY'), 0, '" + summary_text + "','" + party.lower() + "', '" + handle + "');")

#    page_content = currPage.content
    page_content = ''.join(c for c in currPage.content if c not in '\'\";():%')

    word_list = page_content.split()
    word_counter = Counter()
    for word in word_list:
        word_counter[word] += 1

    for word in word_counter:
        count = word_counter[word]
        conn.execute("INSERT INTO wiki_word_aggregate (word,frequency,wiki_page_name) VALUES\
            ('" + word + "'," + str(count) + ",'" + currPage.title + "');")
    
    conn.close()

if __name__ == "__main__":

    lookup_names = [["Hillary Clinton", "hillaryclinton", "Democratic"], ["Donald Trump", "realdonaldtrump", "Republican"], ["Gary Johnson", "govgaryjohnson", "Libertarian"]]

    for lookup_name in lookup_names:
        populate_wiki_tables(lookup_name[0], lookup_name[1], lookup_name[2])

#    populate_wiki_tables("Hillary Clinton", "hillaryclinton", "Democratic")

#    populate_wiki_tables("Hillary Clinton", "hillaryclinton", "Democratic")
#    populate_wiki_tables("Donald Trump", "realdonaldtrump", "Republican")
#    populate_wiki_tables("Gary Johnson", "govgaryjohnson", "Libertarian")

