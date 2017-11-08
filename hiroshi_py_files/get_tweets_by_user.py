try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from collections import Counter

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '3524569402-hWdaeA0moXHixJqWezA9fiajLPgxDY2zQfLHyOD'
ACCESS_SECRET = 'qzEYoPjrQd0lH4tOajCWf1WmiL0TLD99WyTbgO1JAs60O'
CONSUMER_KEY = 'H2sXDISrVwZJIaliuHAKZnlCA'
CONSUMER_SECRET = 'TOfMCt6xnTmh3rbeAGDsMXfxyrjSJA5vnLd8S1DFBB1yvnvJFh'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter = Twitter(auth=oauth)

lookup_handle = "hillaryclinton"

h_tweet = twitter.statuses.user_timeline(screen_name=lookup_handle, count = 5)





class tweet:
    tweet_id = ""
    created_at = ""
    retweet_count = 0
    reply_count = 0
    handle = ""

class twitter_word:
    word = ""
    frequency = 0
    tweet_id = ""

tweet_list = []
twitter_word_list = []


#firstTweet = h_tweet[0]
#tweetText = firstTweet["text"]
#splitText = tweetText.split()
#for oneWord in splitText:
#    print(oneWord)
#    if "http" in oneWord:
#         print("a link.")

for oneTweet in h_tweet:
    tweet_obj = tweet()
    tweet_obj.tweet_id = oneTweet["id_str"]
    tweet_obj.created_at = oneTweet["created_at"]
    print (tweet_obj.created_at)
    tweet_obj.retweet_count = oneTweet["retweet_count"]
    tweet_obj.reply_count = 0 #can't look that up! wtf?
    tweet_obj.handle = lookup_handle
#    print(oneTweet["text"])
    tweet_text = oneTweet["text"]
    wordFreq = Counter()
    for oneWord in tweet_text.split():
        if "http" not in oneWord:
            wordFreq[oneWord] += 1
    for eachWord in wordFreq:
        tweetWord = twitter_word()
        tweetWord.word = eachWord
        tweetWord.frequency = wordFreq[eachWord]
        tweetWord.handle = tweet_obj.tweet_id

#print ("length is: " + len(tweet))

#print json.dumps(h_tweet)


