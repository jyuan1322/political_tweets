# Import the necessary package to process data in JSON format
try:
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

# Initiate the connection to Twitter Streaming API
#twitter_stream = TwitterStream(auth=oauth)
#twitter = Twitter(auth=oauth)
# Get a sample of the public data following through Twitter
#iterator = twitter_stream.search.tweets(q='@hillaryclinton')
#tweet = twitter.statuses(q='@hillaryclinton')
#tweet = twitter.statuses.user_timeline(screen_name="hillaryclinton", count=1)
#user = twitter.users.lookup(screen_name="hillaryclinton");
#print json.dumps(tweet)
# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 1000 tweets. 
# You don't have to set it to stop, but can continue running 
# the Twitter API to collect data for days or even longer. 
#tweet_count = 1
#for tweet in iterator:
#    tweet_count -= 1
   ## Twitter Python Tool wraps the data returned by Twitter 
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
#    print json.dumps(tweet)  

    # The command below will do pretty printing for JSON data, try it out
#print json.dumps(user[0], indent=4)

#    if tweet_count <= 0:
#        break 








class twitter_user:
    handle = ""
    created_at = ""
    follower_count = ""
    location = ""
    url = ""
    profile_image = ""



hillary_t_user = twitter_user()
hillary_t_user.handle = "hillaryclinton"
print("user: " + hillary_t_user.handle)

twitter = Twitter(auth=oauth)
user = twitter.users.show(screen_name = hillary_t_user.handle)
#print json.dumps(user, indent=4)

hillary_t_user.handle = user["screen_name"]
hillary_t_user.created_at = user["created_at"]
hillary_t_user.follower_count = user["followers_count"]
hillary_t_user.url = user["url"]
hillary_t_user.profile_image = user["profile_image_url"]
print(hillary_t_user.__dict__)

