try:
    import json
except ImportError:
    import simplejson as json

import wikipedia
from collections import Counter

class wiki_page:
    name = ""
    dob = ""
    s_score = ""
    summary_text = ""
    political_party = ""
    handle = ""

class wiki_word:
    word = ""
    frequency = ""
    wiki_page_name = ""

handles = ["hillaryclinton", "realdonaldtrump"]

wiki_pages = []

for handle in handles:
    suggestedPage = wikipedia.suggest(handle)
    if suggestedPage == None:
        suggestedPage = handle
    print ("suggested page: " + suggestedPage)
    currPage = wikipedia.page(suggestedPage)
    curr_wiki_page = wiki_page()
    curr_wiki_page.name = currPage.title
    curr_wiki_page.dob = "" #not directly supported
    curr_wiki_page.s_score = 0 #need to calculate
    curr_wiki_page.summary_text = wikipedia.summary(suggestedPage)
    curr_wiki_page.handle = handle
    curr_wiki_page.political_party = "sleepover party" #not directly supported
    
    pageText = currPage.content
    word_list = pageText.split()
    word_counter = Counter()
    for word in word_list:
        word_counter[word] += 1
    for word in word_counter:
        wiki_agg_word = wiki_word()
        wiki_agg_word.word = word
        wiki_agg_word.frequency = word_counter[word]
        wiki_page_name = curr_wiki_page.name

