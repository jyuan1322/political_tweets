# -*- coding: utf-8 -*-
import json
from flask import Flask,render_template,request
from sqlalchemy import *
from pprint import pprint

app = Flask(__name__)

DATABASEURI = "postgresql://jy2732:1833@35.196.90.148/proj1part2"
engine = create_engine(DATABASEURI)
engine.execute("""CREATE TABLE IF NOT EXISTS test (
          id serial,
            name text
            );""")

@app.route('/psqltest')
def psql_test():
    sql = """
        select * from tweet;
    """
    res = engine.execute(sql)
    for row in res:
        print row
    return 'finished query'
    

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/network')
def network():
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
    graph = json.dumps(graph)
    return render_template('network.html',graph=graph)

@app.route('/twitter_word_cloud', methods=['GET','POST'])
def get_word_cloud():
    if request.method == 'POST':
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
        """ % (request.form["twitter_handle"])
        res = engine.execute(sql)
        res = [dict(x) for x in res]
        words = []
        for r in res:
            words.append({'text':str(r['word']),'size':int(r['count'])})
        return render_template('user_word_cloud.html',
                                twitter_user=request.form["twitter_handle"],
                                words=words)
    else:
        return render_template('user_word_cloud.html',twitter_user='',words=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
