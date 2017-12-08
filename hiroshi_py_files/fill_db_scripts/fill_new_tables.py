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

def populate_new_tables ():

    tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app = Flask(__name__, template_folder = tmpl_dir)
    
    DATABASEURI = "postgresql://hf2326:2307@35.196.90.148/proj1part2"

    engine = create_engine(DATABASEURI)
    conn = engine.connect()

    conn.execute("INSERT INTO POLITICIAN_DONATIONS (donate_id, politician_handle, donation) VALUES\
        (1,'realdonaldtrump',('USA SUPER PAC', TO_DATE('08/29/2012', 'MM/DD/YYYY'), 5000.00));")
    conn.execute("INSERT INTO POLITICIAN_DONATIONS (donate_id, politician_handle, donation) VALUES\
        (2,'realdonaldtrump',('AMERICAN CROSSROADS', TO_DATE('10/06/2010', 'MM/DD/YYYY'), 50000.00));")
    conn.execute("INSERT INTO POLITICIAN_DONATIONS (donate_id, politician_handle, donation) VALUES\
        (3,'realdonaldtrump',('JOHN BOLTON SUPER PAC', TO_DATE('07/16/2014', 'MM/DD/YYYY'), 5000.00));")
    conn.execute("INSERT INTO POLITICIAN_DONATIONS (donate_id, politician_handle, donation) VALUES\
        (4,'realdonaldtrump',('CONGRESSIONAL LEADERSHIP FUND', TO_DATE('08/19/2012', 'MM/DD/YYYY'), 100000.00));")
    conn.execute("INSERT INTO POLITICIAN_DONATIONS (donate_id, politician_handle, donation) VALUES\
        (5,'realdonaldtrump',('KENTUCKIANS FOR STRONG LEADERSHIP', TO_DATE('05/21/2013', 'MM/DD/YYYY'), 50000.00));")


    conn.execute("INSERT INTO POLITICIAN_DONATIONS (donate_id, politician_handle, donation) VALUES\
        (6,'hillaryclinton',('HILLARY FOR AMERICA', TO_DATE('04/13/2015', 'MM/DD/YYYY'), 214.81));")
    conn.execute("INSERT INTO POLITICIAN_DONATIONS (donate_id, politician_handle, donation) VALUES\
        (7,'hillaryclinton',('HILLARY FOR AMERICA', TO_DATE('04/13/2015', 'MM/DD/YYYY'), 1488.62));")
    conn.execute("INSERT INTO POLITICIAN_DONATIONS (donate_id, politician_handle, donation) VALUES\
        (8,'hillaryclinton',('HILLARY FOR AMERICA', TO_DATE('04/12/2015', 'MM/DD/YYYY'), 3000.00));")
    conn.execute("INSERT INTO POLITICIAN_DONATIONS (donate_id, politician_handle, donation) VALUES\
        (9,'hillaryclinton',('HILLARY CLINTON FOR PRESIDENT', TO_DATE('11/30/2008', 'MM/DD/YYYY'), 1317500.00));")
    conn.execute("INSERT INTO POLITICIAN_DONATIONS (donate_id, politician_handle, donation) VALUES\
        (10,'hillaryclinton',('HILLARY FOR AMERICA', TO_DATE('05/11/2015', 'MM/DD/YYYY'), 780.00));")


    conn.execute("INSERT INTO POLITICIAN_NEWS (article_id, url, publisher, date_pub, article_title, article_text, politician_handle, tags) VALUES\
        (1, 'https://www.theatlantic.com/magazine/archive/2017/10/will-donald-trump-destroy-the-presidency/537921/', 'The Atlantic', TO_DATE('10/01/2017', 'MM/DD/YYYY'), 'Will Donald Trump Destroy the Presidency?', 'He disdains the rule of law. Hes trampling norms of presidential behavior. And hes bringing vital institutions down with him.', 'realdonaldtrump', '{\"president\",\"behavior\", \"norms\", \"rule of law\"}');")
    conn.execute("INSERT INTO POLITICIAN_NEWS (article_id, url, publisher, date_pub, article_title, article_text, politician_handle, tags) VALUES\
        (2, 'https://www.vanityfair.com/news/2017/04/donald-melania-trump-marriage', 'Vanity Fair', TO_DATE('05/01/2017', 'MM/DD/YYYY'), 'INSIDE THE TRUMP MARRIAGE MELANIAS BURDEN', 'Until November 8, Melinia Trumps marriage provided her with a gold Fifth Avenue fortress', 'realdonaldtrump', '{\"first\",\"lady\",\"public\",\"private\",\"president\"}');")
    conn.execute("INSERT INTO POLITICIAN_NEWS (article_id, url, publisher, date_pub, article_title, article_text, politician_handle, tags) VALUES\
        (3, 'http://www.cnn.com/2017/12/07/politics/donald-trump-approval-rating/index.html', 'CNN', TO_DATE('12/07/2017', 'MM/DD/YYYY'), 'TRUMPS APPROVAL RATING AT 32 PERCENT', 'President Donald Trumps approval rating sits at 32, according to a new poll released by the Pew Research Center, matching the lowest level in any poll on\" his approval since he took office in January.', 'realdonaldtrump', '{\"approval\",\"president\", \"low\",\"disapproval\"}');")
    conn.execute("INSERT INTO POLITICIAN_NEWS (article_id, url, publisher, date_pub, article_title, article_text, politician_handle, tags) VALUES\
        (4, 'https://www.nytimes.com/2017/12/06/us/donald-trump-jr-intel-committee.html', 'NY Times', TO_DATE('12/06/2017', 'MM/DD/YYYY'), 'Trump Jr Wont Provide Details of a Call With His Father', 'Donald Trump Jr. refused on Wednesday to provide a congressional committee details of a July telephone conversation with his father about a meeting last year at which Trump campaign', 'realdonaldtrump', '{\"russia\",\"scandal\",\"hillary\",\"congress\"}');")
    conn.execute("INSERT INTO POLITICIAN_NEWS (article_id, url, publisher, date_pub, article_title, article_text, politician_handle, tags) VALUES\
        (5, 'https://www.economist.com/news/middle-east-and-africa/21732093-campaign-promise-kept-problem-aggravated-world-reacts-donald-trumps', 'The Economist', TO_DATE('12/07/2017', 'MM/DD/YYYY'), 'The world reacts to Donald Trumps recognition of Jerusalem as Isreals capital', 'EVEN before Donald Trump issued his proclamation recognising Jerusalem as the capital of Israel, ', 'realdonaldtrump', '{\"isreal\",\"jerusalem\",\"palestine\",\"middle east\"}');")


    conn.execute("INSERT INTO POLITICIAN_NEWS (article_id, url, publisher, date_pub, article_title, article_text, politician_handle, tags) VALUES\
        (6, 'https://www.nytimes.com/2017/12/07/style/hillary-clinton-lena-dunham-rift-weinstein.html', 'NY Times', TO_DATE('12/07/2017', 'MM/DD/YYYY'), 'Hillary Clinton and Lena Dunham, Her Main Millennial, Hit the Weinstein Wall', 'But early on in a presidential election unlike any other, Ms. Dunham and Mrs. Clinton became a kind of package deal, with the campaign ', 'hillaryclinton', '{\"harvey\",\"weinstein\",\"scandal\",\"disagreement\",\"hillary\"}');")
    conn.execute("INSERT INTO POLITICIAN_NEWS (article_id, url, publisher, date_pub, article_title, article_text, politician_handle, tags) VALUES\
        (7, 'http://nymag.com/daily/intelligencer/2017/05/hillary-clinton-life-after-election.html', 'NY Mag', TO_DATE('05/26/2017', 'MM/DD/YYYY'), 'Hillary Clinton Is Furious. And Resigned. And Funny. And Worried.', 'The surreal post-election life of the woman who would have been president.', 'hillaryclinton', '{\"post-election\",\"interview\",\"hillary\",\"american\"}');")
    conn.execute("INSERT INTO POLITICIAN_NEWS (article_id, url, publisher, date_pub, article_title, article_text, politician_handle, tags) VALUES\
        (8, 'http://www.politifact.com/punditfact/statements/2017/dec/06/puppetstringnewscom/story-misleads-tying-obama-russian-spy-swap-hillar/', 'Politifact', TO_DATE('12/06/2017', 'MM/DD/YYYY'), 'Story misleads tying Obama Russian spy swap to Hillary Clintons Uranium Ore ties', 'A headline points the finger at former President Barack Obama for releasing Russian agents.', 'hillaryclinton', '{\"mislead\",\"news\",\"russia\",\"swap\",\"spy\"}');")
    conn.execute("INSERT INTO POLITICIAN_NEWS (article_id, url, publisher, date_pub, article_title, article_text, politician_handle, tags) VALUES\
        (9, 'https://www.usatoday.com/story/news/politics/onpolitics/2017/12/07/hillary-clinton-goes-tweetstorm/931680001/', 'USA Today', TO_DATE('12/07/2017', 'MM/DD/YYYY'), 'Hillary Clinton criticizes Congress over fate of childrens health insurance program', 'Hillary Clinton isnt exactly known for going on tweetstorms, but she still turned to Twitter to vent her frustrat', 'hillaryclinton', '{\"health\",\"children\",\"hillary\",\"twitter\",\"insurance\"}');")
    conn.execute("INSERT INTO POLITICIAN_NEWS (article_id, url, publisher, date_pub, article_title, article_text, politician_handle, tags) VALUES\
        (10, 'https://www.vanityfair.com/news/2017/11/what-hillary-clinton-got-wrong-about-fox-news', 'Vanity Fair', TO_DATE('11/11/1111', '11/21/2017'), 'WHAT HILLARY CLINTON GOT WRONG ABOUT FOX NEWS', 'Hillary Clinton tends to hate the press in a bipartisan fashion. Shes got reason to be suspicious, given the battering shes taken over several decades. But shes now gone a', 'hillaryclinton', '{\"fox\",\"news\",\"media\",\"bill\",\"clinton\"}');")

    conn.close()


if __name__ == "__main__":


    populate_new_tables()
