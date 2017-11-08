NSERT INTO political_party (name,agg_sentiment_score)
    VALUES ('Democratic',0.3),
            ('Republican',0.3),
            ('Libertarian',0.1),
            ('Green',0.2),
            ('Other',0.1);

INSERT INTO twitter_user (handle,created_at,follower_count,location,url,profile_image) VALUES
    ('@HillaryClinton',TO_DATE('07/04/2008','DD/MM/YYYY'),345000,'New York, NY','https://twitter.com/HillaryClinton','https://pbs.twimg.com/profile_images/839938827837976576/leN1zJJx_400x400.jpg'),
    ('@realDonaldTrump',TO_DATE('03/01/2009','MM/DD/YYYY'),40500000,'Washington, DC','https://twitter.com/realDonaldTrump','https://pbs.twimg.com/profile_images/874276197357596672/kUuht00m_400x400.jpg'),
    ('@GovGaryJohnson',TO_DATE('12/01/2009','MM/DD/YYYY'),345000,'New Mexico','https://twitter.com/GovGaryJohnson','https://pbs.twimg.com/profile_images/785511245424254977/6BGNCTXo_400x400.jpg');

INSERT INTO tweet (tweet_id,created_at,retweet_count,reply_count,handle) VALUES
    ('924635926714105264',TO_DATE('04/02/2017','DD/MM/YYYY'),11384,230,'@HillaryClinton'),
    ('495020116012039865',TO_DATE('04/01/2017','DD/MM/YYYY'),9093,124,'@HillaryClinton'),
    ('391315209125974410',TO_DATE('03/28/2017','DD/MM/YYYY'),8459,232,'@HillaryClinton'),
    ('354422042678131208',TO_DATE('03/26/2017','DD/MM/YYYY'),1456,450,'@HillaryClinton'),
    ('918806396875010048',TO_DATE('10/13/2017','MM/DD/YYYY'),11487,11000,'@realDonaldTrump'),
    ('918808798059483136',TO_DATE('10/13/2017','MM/DD/YYYY'),7052,17000,'@realDonaldTrump'),
    ('918797009133465600',TO_DATE('10/13/2017','MM/DD/YYYY'),9053,18000,'@realDonaldTrump'),
    ('918796079243677696',TO_DATE('10/13/2017','MM/DD/YYYY'),6924,9900,'@realDonaldTrump'),
    ('913421214525169666',TO_DATE('09/28/2017','MM/DD/YYYY'),189,35,'@GovGaryJohnson'),
    ('913051661026836480',TO_DATE('09/27/2017','MM/DD/YYYY'),610,55,'@GovGaryJohnson'),
    ('891302188386889732',TO_DATE('07/29/2017','MM/DD/YYYY'),276,199,'@GovGaryJohnson'),
    ('889870145279143936',TO_DATE('07/25/2017','MM/DD/YYYY'),91,23,'@GovGaryJohnson'),
    ('918885859230875649',TO_DATE('10/13/2017','MM/DD/YYYY'),3916,7500,'@realDonaldTrump'),
    ('918647067224035334',TO_DATE('10/12/2017','MM/DD/YYYY'),12912,18000,'@realDonaldTrump'),
    ('918275261011038210',TO_DATE('10/11/2017','MM/DD/YYYY'),12864,11000,'@realDonaldTrump');

INSERT INTO twitter_word (word,frequency,tweet_id) VALUES
    ('call',1,'924635926714105264'),
    ('your',1,'924635926714105264'),
    ('senator',2,'924635926714105264'),
    ('need',1,'924635926714105264'),
    ('hope',2,'495020116012039865'),
    ('need',3,'495020116012039865'),
    ('you','2','495020116012039865'),
    ('hard','1','918806396875010048'),
    ('believe','1','918806396875010048'),
    ('democrat','1','918806396875010048'),
    ('far','1','918806396875010048'),
    ('wonderful','1','918808798059483136'),
    ('unmatched','1','918808798059483136'),
    ('broken','1','918797009133465600'),
    ('mess','1','918797009133465600'),
    ('sadly','1','918796079243677696'),
    ('fake','1','918796079243677696'),
    ('no-brainer','1','913421214525169666'),
    ('repeal','1','913421214525169666'),
    ('refusing','1','913051661026836480'),
    ('crazy','1','913051661026836480'),
    ('friend','1','891302188386889732'),
    ('agree','1','891302188386889732'),
    ('beleaguered','1','889870145279143936'),
    ('hope','1','889870145279143936');

INSERT INTO hashtag (name,total_twitter_freq) VALUES
    ('#ItTakesAVillage',143),
    ('#JonesAct',5642),
    ('#PuertoRico',15567),
    ('#JeffSessions',1239),
        ('#CivilForfeiture',984),
    ('#Liberty',167879),
    ('#USVI',245),
    ('#PuertoRicoRelief',9854),
    ('#USA',993874),
    ('#TaxReform',85745),
    ('#ValuesVotersSummit',3840);

INSERT INTO hashtag_member (name,tweet_id) VALUES
    ('#ItTakesAVillage','924635926714105264'),
    ('#JonesAct','913421214525169666'),
    ('#PuertoRico','913421214525169666'),
    ('#JeffSessions','889870145279143936'),
    ('#CivilForfeiture','889870145279143936'),
    ('#Liberty','889870145279143936'),
    ('#USVI','913051661026836480'),
    ('#PuertoRicoRelief','913051661026836480'),
    ('#USA','918275261011038210'),
    ('#TaxReform','918647067224035334'),
    ('#ValuesVotersSummit','918885859230875649');

INSERT INTO wikipedia_page (wiki_page_name,name,date_of_birth,sentiment_score,summary_text,political_party,handle) VALUES
    ('Hillary_Clinton','Hillary Clinton',TO_DATE('26/10/1947','DD/MM/YYYY'),0.3,'Hillary Diane Rodham Clinton (/ˈhɪləri daɪˈæn ˈrɒdəm ˈklɪntən/; born October 26, 1947) is an American politician who was the First Lady of the United States from 1993 to 2001, U.S. Senator from New York from 2001 to 2009, 67th United States Secretary of State from 2009 to 2013, and the Democratic Party''s nominee for President of the United States in the 2016 election.','Democratic','@HillaryClinton'),
    ('Donald_Trump','Donald John Trump',TO_DATE('06/14/1946','MM/DD/YYYY'),0.2,'Donald John Trump (born June 14, 1946) is the 45th and current President of the United States, in office since January 20, 2017. Before entering politics, he was a businessman and television personality.','Republican','@realDonaldTrump'),
    ('Gary_Johnson','Gary Earl Johnson',TO_DATE('01/01/1953','MM/DD/YYYY'),0.4,'Gary Earl Johnson (born January 1, 1953) is an American businessman, author, and politician. He was the 29th Governor of New Mexico from 1995 to 2003 as a member of the Republican Party. He was also the Libertarian Party nominee for President of the United States in the 2012 and 2016 elections.','Libertarian','@GovGaryJohnson');

INSERT INTO wiki_word_aggregate (word,frequency,wiki_page_name) VALUES
    ('senator',23,'Hillary_Clinton'),
    ('email',31,'Hillary_Clinton'),
    ('women',68,'Hillary_Clinton'),
    ('speech',39,'Hillary_Clinton'),
    ('benghazi',26,'Hillary_Clinton'),
    ('power',31,'Hillary_Clinton'),
    ('need',6,'Hillary_Clinton'),
    ('protest',26,'Donald_Trump'),
    ('populist',6,'Donald_Trump'),
    ('history',22,'Donald_Trump'),
    ('repeal',11,'Donald_Trump'),
    ('climate',13,'Donald_Trump'),
    ('russia',23,'Donald_Trump'),
    ('democrat',24,'Donald_Trump'),
    ('believe',1,'Donald_Trump'),
    ('veto',17,'Gary_Johnson'),
    ('anti',16,'Gary_Johnson'),
    ('libertarian',74,'Gary_Johnson'),
    ('drug',13,'Gary_Johnson'),
    ('repeal',2,'Gary_Johnson');
