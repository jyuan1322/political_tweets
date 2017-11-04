import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '3524569402-hWdaeA0moXHixJqWezA9fiajLPgxDY2zQfLHyOD'
ACCESS_SECRET = 'qzEYoPjrQd0lH4tOajCWf1WmiL0TLD99WyTbgO1JAs60O'
CONSUMER_KEY = 'H2sXDISrVwZJIaliuHAKZnlCA'
CONSUMER_SECRET = 'TOfMCt6xnTmh3rbeAGDsMXfxyrjSJA5vnLd8S1DFBB1yvnvJFh'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter = Twitter(auth=oauth)

tweet = twitter.statuses.user_timeline(screen_name="hillaryclinton", count = 1)





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


