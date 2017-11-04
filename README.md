# political_tweets


A note about running this on google cloud: to enable HTTP/S connections, 
in console go to NETWORKING: VPC network. Then create a Firewall rule, and
give it a tag, i.e. 'flask-connect'. Then click on your project, and click
'eddit'. Under 'Network tags', add the firewall tag.


get word cloud for a single twitter stream
TO DO:
grab for a whole political party
grab for a hashtag?
grab for wikipedia page

get sentiment score for a single twitter stream
see example script or this link:
https://github.com/cjhutto/vaderSentiment/issues/8

get network of relatedness between twitter streams
