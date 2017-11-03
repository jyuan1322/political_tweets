# political_tweets


A note about running this on google cloud: to enable HTTP/S connections, 
in console go to NETWORKING: VPC network. Then create a Firewall rule, and
give it a tag, i.e. 'flask-connect'. Then click on your project, and click
'eddit'. Under 'Network tags', add the firewall tag.
