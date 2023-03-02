import re
import os
import hashlib
from datetime import datetime
import pandas as pd
import snscrape.modules.twitter as twitter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def regex(word):
    word = re.sub(r'\s+', ' ', word)
    return word

maxTweets = 100
with open('company_url.txt') as f:
    lines = f.readlines()
for query in lines:
# query = '$PG'
    tweets_list = []
    for i, tweet in enumerate(twitter.TwitterSearchScraper(query).get_items(),1):
        if i > maxTweets:
            break 
        json_res=tweet.json
        dir_path = os.path.join(os.getcwd(), 'html/')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        hash_obj = hashlib.md5(f"{query}".encode('utf-8'))
        filename = hash_obj.hexdigest()

        with open(dir_path+f"{filename}.txt", "w", encoding='utf-8') as img:
            img.write(str(json_res))
        
        # with open("check.txt","w")as f: f.write(str(json_res))
        items = {}
        items['date_of_post'] = tweet.date.strftime('%d/%m/%Y')
        # items['time'] = tweet.date.strftime('%H:%M')
        items['username'] = tweet.user.displayname
        handle_name = tweet.user.username
        if handle_name:
            items['handle'] = '@'+handle_name
        else:
            items["handle_name"] = ''
        items['post'] = regex(tweet.content.strip())
        items['post_url'] = tweet.url
        items['twitter_profile_url'] = tweet.url.split('status')[0]
        items['number_of_followers'] = tweet.user.followersCount
        print(items['username'])
        items['search_keywords'] = query.strip()
        df = pd.DataFrame([items])
        if handle_name:
            items['handle'] = '@'+handle_name
            if not os.path.isfile("twitter_sample.csv"):
                df.to_csv("twitter_sample.csv",index=False,mode="a",header=True,encoding="utf_8_sig",)
            else:  # else it exists so append without writing the header
                df.to_csv("twitter_sample.csv",mode="a",header=False,index=False,encoding="utf_8_sig",)
          