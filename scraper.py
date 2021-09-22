'''
@author: Souvik Das
Institute: University at Buffalo
'''

import json
import datetime
import pandas as pd
from twitter import Twitter
from tweet_preprocessor import TWPreprocessor
from indexer import Indexer

reply_collection_knob = False


def read_config():
    with open("config.json") as json_file:
        data = json.load(json_file)

    return data


def write_config(data):
    with open("config.json", 'w') as json_file:
        json.dump(data, json_file)


def save_file(data, filename):
    df = pd.DataFrame(data)
    df.to_pickle("data/" + filename)


def read_file(type, id):
    return pd.read_pickle(f"data/{type}_{id}.pkl")


def main():
    config = read_config()
    indexer = Indexer()
    twitter = Twitter()

    pois = config["pois"]
    keywords = config["keywords"]

    for i in range(len(pois)):
        if pois[i]["finished"] == 0:
            print(f"---------- collecting tweets for poi: {pois[i]['screen_name']}")

            raw_tweets = twitter.get_tweets_by_poi_screen_name(pois[i]["screen_name"], pois[i]["count"])  # pass args as needed

            processed_tweets = []
            for tw in raw_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw,pois[i]['country']))

            indexer.create_documents(processed_tweets)

            pois[i]["finished"] = 1
            pois[i]["collected"] = len(processed_tweets)

            write_config({
                "pois": pois, "keywords": keywords
            })

            save_file(processed_tweets, f"poi_{pois[i]['id']}.pkl")
            print("------------ process complete -----------------------------------")
'''
    for i in range(len(keywords)):
        if keywords[i]["finished"]==0:
            print(f"---------- collecting tweets for keyword: {keywords[i]['name']}")

            raw_tweets = twitter.get_tweets_by_lang_and_keyword(keywords[i]['name'],keywords[i]['lang'],keywords[i]['count'])  # pass args as needed

            processed_tweets = []
            for tw in raw_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw,is_keyword=True))

            indexer.create_documents(processed_tweets)

            keywords[i]["finished"] = 1
            keywords[i]["collected"] = len(processed_tweets)

            write_config({
                "pois": pois, "keywords": keywords
            })

            save_file(processed_tweets, f"keywords_{keywords[i]['id']}.pkl")

            print("------------ process complete -----------------------------------")

    if reply_collection_knob:
        # Write a driver logic for reply collection, use the tweets from the data files for which the replies are to collected.
        preprocessed_tweets=[]
        count=0
        for words in keywords:
            if(words['lang']=='en' and count<10000):
                keyWords_tweets = read_file('keywords',words['id'])
                for tweet in keyWords_tweets.to_dict(orient='records'):
                    status = twitter.api.get_status(tweet['id'])
                    user = status.user.screen_name
                    raw_tweets = twitter.get_replies(tweet_id,None,user,100)
                    for tweet in raw_tweets:
                        count+=1
                        preprocessed_tweets.append(TWPreprocessor.preprocess(tweet,isreply=True))
            else:
                break
    
        save_file(preprocessed_tweets, "reply_tweets.pkl")

        indexer.create_documents(preprocessed_tweets)'''



if __name__ == "__main__":
    main()
