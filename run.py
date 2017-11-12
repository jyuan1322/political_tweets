# -*- coding: utf-8 -*-
import json, datetime
from flask import Flask,render_template,request,jsonify
from sqlalchemy import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pprint import pprint

app = Flask(__name__)

DATABASEURI = "postgresql://jy2732:1833@35.196.90.148/proj1part2"
engine = create_engine(DATABASEURI)

@app.route('/')
def hello_world():
    return render_template("main_menu.html")

@app.route('/sentiment_time')
def sentiment_time():
    sql = """
        SELECT DISTINCT T.handle,T.tweet_id,TW.word,T.created_at
        FROM tweet T, twitter_word TW
        WHERE T.tweet_id = TW.tweet_id
    """
    res = engine.execute(sql)
    res = [dict(x) for x in res]

    handles = {}
    twitter_start = float('inf')
    twitter_end = float('-inf')
    for r in res:
        handle = r['handle']
        if handle not in handles:
            handles[handle] = {}
        epoch = datetime.date(1970,1,1)
        tdate = (r['created_at']-epoch).total_seconds() * 1000
        if tdate < twitter_start:
            twitter_start = tdate
        if tdate > twitter_end:
            twitter_end = tdate
        if tdate not in handles[handle]:
            handles[handle][tdate] = ""
        handles[handle][tdate] += " " + r['word']
    pprint(handles)
    
    analyzer = SentimentIntensityAnalyzer()
    lines = []
    for h in handles:
        line = []
        for d in handles[h]:
            line.append([d,analyzer.polarity_scores(handles[h][d])["compound"]])
        line.sort(key=lambda x:x[0])
        lines.append({"name":h,"line":line})
    pprint(lines)

    return render_template('sentiment_time.html', lines=lines,twitter_start=twitter_start,twitter_end=twitter_end,twitter_minscore=-1,twitter_maxscore=1)

@app.route('/network')
def network():
    sql = """
        SELECT AA.handle as u1,BB.handle as u2,AA.word,AA.wc as c1,BB.wc as c2,
                AA.political_party as p1, BB.political_party as p2
        FROM
            (SELECT A.handle,A.political_party,B.word,COUNT(B.word) as wc
            FROM
                    (SELECT TU.handle, WW.political_party
                    FROM twitter_user TU, wikipedia_page WW
                    WHERE TU.handle = WW.handle) A
            JOIN
                    (SELECT DISTINCT T.handle,T.tweet_id,TW.word
                    FROM tweet T, twitter_word TW
                    WHERE T.tweet_id = TW.tweet_id) B
            ON A.handle = B.handle
            GROUP BY A.handle,A.political_party,B.word
            HAVING COUNT(B.word) > 1) AA
        JOIN
            (SELECT A.handle,A.political_party,B.word,COUNT(B.word) as wc
            FROM
                    (SELECT TU.handle, WW.political_party
                    FROM twitter_user TU, wikipedia_page WW
                    WHERE TU.handle = WW.handle) A
            JOIN
                    (SELECT DISTINCT T.handle,T.tweet_id,TW.word
                    FROM tweet T, twitter_word TW
                    WHERE T.tweet_id = TW.tweet_id) B
            ON A.handle = B.handle
            GROUP BY A.handle,A.political_party,B.word
            HAVING COUNT(B.word) > 1) BB
        ON AA.word = BB.word
        WHERE AA.handle != BB.handle AND AA.handle < BB.handle;
    """
    res = engine.execute(sql)
    res = [dict(x) for x in res]
    pprint(res)
    
    nodes = []
    links = []
    pol_parties = {}
    inc = 0
    for r in res:
        u1 = r["u1"]
        u2 = r["u2"]
        node_ids = [x["id"] for x in nodes]
        if u1 not in node_ids:
            if r["p1"] not in pol_parties:
                pol_parties[r["p1"]] = inc
                inc += 1
            nodes.append({"id":u1, "group":pol_parties[r["p1"]]})
        if u2 not in node_ids:
            if r["p2"] not in pol_parties:
                pol_parties[r["p2"]] = inc
                inc += 1
            nodes.append({"id":u2, "group":pol_parties[r["p2"]]})
        links.append({"source":u1,"target":u2,"value":min(r["c1"],r["c2"])})
    graph = {"nodes":nodes,"links":links}
    pprint(graph)
    """
    graph = {
                "nodes": [
                    {"id":"Hillary", "group":1},
                    {"id":"Trump", "group":2},
                    {"id":"Ford", "group":2}
                    ],
                "links": [
                    {"source":"Hillary", "target":"Trump", "value":1},
                    {"source":"Hillary", "target":"Ford", "value":10}
                    ]}
    """
    graph = json.dumps(graph)
    return render_template('network.html',graph=graph)

@app.route('/twitter_word_cloud', methods=['GET','POST'])
def get_word_cloud():
    sql = """
        SELECT handle,name
        FROM wikipedia_page
    """
    options = engine.execute(sql)
    options = [dict(x) for x in options]

    if request.method == 'POST':
        res,words = word_cloud_sql(request.form["twitter_handle"])

        res_str = []
        for r in res:
            for i in range(int(r['count'])):
                res_str.append(r['word'])
        res_str = " ".join(res_str)
        analyzer = SentimentIntensityAnalyzer()
        sentiment = analyzer.polarity_scores(res_str)["compound"]

        print "selected:", request.form["twitter_handle"]

        return render_template('user_word_cloud.html',
                                twitter_user=request.form["twitter_handle"],
                                sentiment=sentiment,
                                options=options,
                                words=words)
    else:
        return render_template('user_word_cloud.html',twitter_user='',options=options,words=None)

def word_cloud_sql(twitter_handle):
    sql = """
        SELECT A.handle,B.word,COUNT(B.word)
        FROM
                (SELECT TU.handle, WW.political_party
                FROM twitter_user TU, wikipedia_page WW
                WHERE TU.handle = WW.handle) A
        JOIN
                (SELECT DISTINCT T.handle,T.tweet_id,TW.word
                FROM tweet T, twitter_word TW
                WHERE T.tweet_id = TW.tweet_id) B
        ON A.handle = B.handle
        WHERE A.handle = '%s'
        GROUP BY A.handle,B.word;
    """ % (twitter_handle)
    res = engine.execute(sql)
    res = [dict(x) for x in res]
    words = []
    for r in res:
        words.append({'text':str(r['word'].encode('utf-8')),'size':int(r['count'])})
    return res,words

@app.route('/get_values', methods=['GET','POST'])
def get_values():
    twitter_handle = request.get_data()
    print "twitter_handle:", twitter_handle
    result = "Last updated: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    res, new_wc_words = word_cloud_sql(twitter_handle)
    return jsonify(result=result,new_wc_words=new_wc_words)

# -------------------------------------------------------------------

@app.route('/twitter_party_word_cloud', methods=['GET','POST'])
def get_party_word_cloud():
    sql = """
        SELECT name
        FROM political_party
    """
    options = engine.execute(sql)
    options = [dict(x) for x in options]

    if request.method == 'POST':
        res,words = party_word_cloud_sql(request.form["pol_party"])

        res_str = []
        for r in res:
            for i in range(int(r['count'])):
                res_str.append(r['word'])
        res_str = " ".join(res_str)
        analyzer = SentimentIntensityAnalyzer()
        sentiment = analyzer.polarity_scores(res_str)["compound"]

        print "selected:", request.form["pol_party"]

        return render_template('party_word_cloud.html',
                                pol_party=request.form["pol_party"],
                                sentiment=sentiment,
                                options=options,
                                words=words)
    else:
        return render_template('party_word_cloud.html',pol_party='',options=options,words=None)

def party_word_cloud_sql(pol_party):
    sql = """
        SELECT A.political_party,B.word,COUNT(B.word)
        FROM
                (SELECT WW.handle,WW.political_party
                FROM wikipedia_page WW) A
        JOIN
                (SELECT DISTINCT T.handle,T.tweet_id,TW.word
                FROM tweet T, twitter_word TW
                WHERE T.tweet_id = TW.tweet_id) B
        ON A.handle = B.handle
        WHERE A.political_party = '%s'
        GROUP BY A.political_party,B.word;
    """ % (pol_party)
    res = engine.execute(sql)
    res = [dict(x) for x in res]
    words = []
    for r in res:
        words.append({'text':str(r['word'].encode('utf-8')),'size':int(r['count'])})
    return res,words

@app.route('/get_party_values', methods=['GET','POST'])
def get_party_values():
    pol_party = request.get_data()
    print "pol_party:", pol_party
    result = "Last updated: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    res, new_wc_words = party_word_cloud_sql(pol_party)
    return jsonify(result=result,new_wc_words=new_wc_words)

# -------------------------------------------------------------------

@app.route('/wiki_word_cloud', methods=['GET','POST'])
def get_wiki_word_cloud():
    sql = """
        SELECT wiki_page_name as wiki_name
        FROM wikipedia_page
    """
    options = engine.execute(sql)
    options = [dict(x) for x in options]

    if request.method == 'POST':
        res,words = wiki_word_cloud_sql(request.form["wiki_name"])

        res_str = []
        for r in res:
            for i in range(int(r['count'])):
                res_str.append(r['word'])
        res_str = " ".join(res_str)
        analyzer = SentimentIntensityAnalyzer()
        sentiment = analyzer.polarity_scores(res_str)["compound"]

        print "selected:", request.form["wiki_name"]

        return render_template('wiki_word_cloud.html',
                                wiki_name=request.form["wiki_name"],
                                sentiment=sentiment,
                                options=options,
                                words=words)
    else:
        return render_template('wiki_word_cloud.html',wiki_party='',options=options,words=None)

def wiki_word_cloud_sql(wiki_name):
    sql = """
        SELECT A.wiki_page_name,A.word,A.frequency as count
        FROM
                wiki_word_aggregate A
        WHERE A.wiki_page_name = '%s'
    """ % (wiki_name)
    res = engine.execute(sql)
    res = [dict(x) for x in res]
    words = []
    for r in res:
        words.append({'text':str(r['word'].encode('utf-8')),'size':int(r['count'])})
    return res,words

# -------------------------------------------------------------------

@app.route('/hashtag_word_cloud', methods=['GET','POST'])
def get_hashtag_word_cloud():
    sql = """
        SELECT name
        FROM hashtag
    """
    options = engine.execute(sql)
    options = [dict(x) for x in options]

    if request.method == 'POST':
        res,words = hashtag_word_cloud_sql(request.form["hashtag"])

        res_str = []
        for r in res:
            for i in range(int(r['count'])):
                res_str.append(r['word'])
        res_str = " ".join(res_str)
        analyzer = SentimentIntensityAnalyzer()
        sentiment = analyzer.polarity_scores(res_str)["compound"]

        print "selected:", request.form["hashtag"]

        return render_template('hashtag_word_cloud.html',
                                hashtag=request.form["hashtag"],
                                sentiment=sentiment,
                                options=options,
                                words=words)
    else:
        return render_template('hashtag_word_cloud.html',hashtag='',options=options,words=None)

def hashtag_word_cloud_sql(hashtag):
    sql = """
        SELECT A.name,B.word,COUNT(B.word)
        FROM
                (SELECT HM.name, HM.tweet_id
                FROM hashtag_member HM) A
        JOIN
                (SELECT TW.word,TW.tweet_id
                FROM twitter_word TW) B
        ON A.tweet_id = B.tweet_id
        WHERE A.name = '%s'
        GROUP BY A.name,B.word;
    """ % (hashtag)
    res = engine.execute(sql)
    res = [dict(x) for x in res]
    words = []
    for r in res:
        words.append({'text':str(r['word'].encode('utf-8')),'size':int(r['count'])})
    return res,words

@app.route('/get_hashtag_values', methods=['GET','POST'])
def get_hashtag_values():
    hashtag = request.get_data()
    print "hashtag:", hashtag
    result = "Last updated: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    res, new_wc_words = hashtag_word_cloud_sql(hashtag)
    return jsonify(result=result,new_wc_words=new_wc_words)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
