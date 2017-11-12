try:
    import json
except ImportError:
    import simplejson as json

import wikipedia
from collections import Counter
import os,sys
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

def populate_wiki_tables (lookup_name, handle, party):

    tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app = Flask(__name__, template_folder = tmpl_dir)
    
    DATABASEURI = "postgresql://jy2732:1833@35.196.90.148/proj1part2"

    engine = create_engine(DATABASEURI)
    conn = engine.connect()

    party=party.lower()
    sql = """
            INSERT INTO political_party (name)
            SELECT '%s'
            WHERE NOT EXISTS (
                SELECT 1 FROM political_party
                WHERE name = '%s'
            );
    """ % (party,party)
    conn.execute(sql)
    """
    conn.execute("INSERT INTO POLITICAL_PARTY (name) \
        SELECT '" + party.lower() + "' WHERE NOT EXISTS (SELECT * FROM POLITICAL_PARTY WHERE name = '" + party + "');")
    """

    lookup_name=lookup_name.lower()
    handle = handle.lower()

    suggestedPage = wikipedia.suggest(lookup_name)

    if suggestedPage == None:
        suggestedPage = lookup_name

    currPage = wikipedia.page(suggestedPage)
    summary_text = ''.join(c for c in wikipedia.summary(suggestedPage) if c not in '\'\";():%')

    sql = """
            INSERT INTO wikipedia_page (wiki_page_name,name,date_of_birth,sentiment_score,summary_text,political_party,handle)
            SELECT '%s',
                    '%s',
                    TO_DATE('1/1/2017', 'DD/MM/YYYY'),
                    0,
                    '%s',
                    '%s',
                    '%s'
            WHERE NOT EXISTS (
                SELECT 1 FROM wikipedia_page
                WHERE wiki_page_name = '%s'
            );
    """ % (currPage.title,
            suggestedPage,
            summary_text,
            party,
            handle,
            currPage.title)
    conn.execute(sql)
    """
    conn.execute("INSERT INTO wikipedia_page (wiki_page_name,name,date_of_birth,sentiment_score,summary_text,political_party,handle) VALUES \
        ('" + currPage.title + "','" + suggestedPage + "', TO_DATE('1/1/2017', 'DD/MM/YYYY'), 0, '" + summary_text + "','" + party.lower() + "', '" + handle + "');")
    """

    page_content = ''.join(c for c in currPage.content if c not in '\'\";():%,.')

    word_list = page_content.split()
    word_counter = Counter()
    for word in word_list:
        word_counter[word] += 1

    for word in word_counter:
        count = word_counter[word]
        sql = """
                INSERT INTO wiki_word_aggregate (word,frequency,wiki_page_name)
                SELECT '%s',
                        %s,
                        '%s'
                WHERE NOT EXISTS (
                    SELECT 1 FROM wiki_word_aggregate
                    WHERE wiki_page_name='%s' AND word='%s'
                );
        """ % (word,str(count),currPage.title,currPage.title,word)
        conn.execute(sql)
        """
        conn.execute("INSERT INTO wiki_word_aggregate (word,frequency,wiki_page_name) VALUES\
            ('" + word + "'," + str(count) + ",'" + currPage.title + "');")
        """
    conn.close()

def populate_wiki_db():
    populate_wiki_tables("Hillary Clinton", "hillaryclinton", "Democratic")
    populate_wiki_tables("Donna Brazile", "donnabrazile", "Democratic")
    populate_wiki_tables("Donald Trump", "realdonaldtrump", "Republican")
    populate_wiki_tables("Gary Johnson", "govgaryjohnson", "Libertarian")


if __name__ == "__main__":

    populate_wiki_db()
    sys.exit(0)

    lookup_names = [["Hillary Clinton", "hillaryclinton", "Democratic"], ["Donald Trump", "realdonaldtrump", "Republican"], ["Gary Johnson", "govgaryjohnson", "Libertarian"]]

    for lookup_name in lookup_names:
        populate_wiki_tables(lookup_name[0], lookup_name[1], lookup_name[2])

#    populate_wiki_tables("Hillary Clinton", "hillaryclinton", "Democratic")

#    populate_wiki_tables("Hillary Clinton", "hillaryclinton", "Democratic")
#    populate_wiki_tables("Donald Trump", "realdonaldtrump", "Republican")
#    populate_wiki_tables("Gary Johnson", "govgaryjohnson", "Libertarian")
