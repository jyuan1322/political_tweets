# Political Tweet Analyzer

Jie Yuan (jy2732)
Hiroshi Furuya (hf2326)



For visualization, we have borrowed heavily from existing implementations in D3.js and other resources. Most of these are listed below:

Word Cloud visualization:
https://github.com/jasondavies/d3-cloud

Network visualization:
https://bl.ocks.org/mbostock/4062045

Legend generation in line plot:
http://bl.ocks.org/ZJONSSON/3918369

Pre-trained sentiment analyzer:
https://github.com/cjhutto/vaderSentiment




1. The postgres database (jy2732) can be accessed at:
psql -U jy2732 -h 35.196.90.148 -d proj1part2



2. When launched, the URL of the home page of the web application will be:
http://[server-ip]:5000/

As of submission, this URL is
http://35.190.190.32:5000/

However, as this is a temporary external IP address of our google cloud instance, the instance may be shut down in the future, or the external IP address may change.


3. We stated in Part 1 that we were to build a web application for real-time analysis and visualization of political tweets between Democrats and Republicans. Features mentioned included word clouds, sentiment analysis, and a network view of word similarity between individuals. 

We have implemented all of the promised features, with the exception of the real-time updates, which is half-functional. We have provided scripts for automatic retrieval of Twitter and Wikipedia text from their respective APIs, and most of our word cloud pages (excluding Wikipedia due to data retrieval size) feature an automatic refresh. The only step to make this fully real-time would be to run the script at each refresh, but we opted against this becaues of Twitter's API call limit: 15 calls per 15 minutes. To guarantee that these API calls are returned, only one call can be made per minute, which is too slow for demonstration. Additionally, we were concerned that errors in rejected calls combined with the automatic refresh would increase the chance of execution errors in our Flask app.

We have included word clouds for individual politicians, all politicians belonging to a particular political party, Wikipedia pages for individual politicians, and all tweets associated with a given hashtag. Additionally, we have included a sentiment analysis score for the words included in each word cloud.

We have also included a network visualization using D3.js, in which nodes are individual politicians colored according to their political party, and edges between nodes are the sum of shared words between the Twitter accounts of politicians. This graph starts to become interesting once more individuals are added (we currently have 4), however we have opted against this to ensure that the data is a small size for demonstration. Adding politicians is easy: simply run our script Twitter and Wikipedia scraping scripts with a Twitter handle, Wikipedia article title, and a manually-assigned political party, and the returned data will be automatically inserted into our database.

Lastly, we have added a sentiment plot over time for each politician in our database. Each data point is a single tweet sent at a particular time (x-axis), with the sentiment score of the included words on the y-axis.

4. Most of the word clouds involve a similar SQL query in which a particular Twitter handle is extracted from our table of twitter users and then joined with the words that that individual has tweeted. To ensure a lack of data redundancy, individual tweets are assigned their own table, and the words comprising those tweets are given their own separate table, with an id associating them back to the tweet. Therefore, multiple joins are used to link a Twitter handle to the tweets that that handle has produced, and then the words that are used in those tweets. After these are collected, the words are grouped in order to achieve a count across all tweets (as an important word overwhelmingly occurs only once in a tweet, to improve execution time we decided to extract one occurrence of a word from each tweet). A table of words and their counts are then sent to the frontend, which displays a word cloud in which the size of the word is scaled according to its frequency.

Another rather complicated tweet is the one used to compare word usage between two individuals in the network visualization. A query similar to the one used to extract word usage is run twice and then joined together by the word, and the two pairs of Twitter handles are ordered alphabetically to remove duplicates and self-matches. Then, for each row which now consists of two nodes, and an edge strength specified by the min word frequency between the two handles, is sent to the frontend to specify the network architecture. 





A note about running this on google cloud: to enable HTTP/S connections, 
in console go to NETWORKING: VPC network. Then create a Firewall rule, and
give it a tag, i.e. 'flask-connect'. Then click on your project, and click
'edit'. Under 'Network tags', add the firewall tag.

