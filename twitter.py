'''
@author: Souvik Das
Institute: University at Buffalo
'''

import tweepy


class Twitter:
    def __init__(self):
        sself.auth = tweepy.OAuthHandler("N22EJJVNjn0CtdK2uFDEUM4GL", "VKOWeNHY3BhuGObwMLFMui86FFT2GECNE1ue42z1HjqIXBsvdA")
        self.auth.set_access_token("1432475992413687809-cKUxOzJBop2jDMVfDCf9LvtwXhi6ti", "QSIH5e46bpWurFDt7kiPXTMCxPjWn9CtIGdIfmU4NtPgT")
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


    def get_tweets_by_poi_screen_name(self,poiName,count):
        '''
        Use user_timeline api to fetch POI related tweets, some postprocessing may be required.
        :return: List
        '''
        _list=[]
        for tweet in tweepy.Cursor(self.api.user_timeline,screen_name=poiName).items(count):
            _list.append(tweet)
        return _list

    def get_tweets_by_lang_and_keyword(self,keyword,lang,count):
        '''
        Use search api to fetch keywords and language related tweets, use tweepy Cursor.
        :return: List
        '''
        _list=[]
        for tweets in tweepy.Cursor(self.api.search,keyword,lang).items(count):
            #print(type(tweets))
            _list.append(tweets)
        return _list

    def get_replies(self,tweet_id,sinceID,user,maxID):
        '''
        Get replies for a particular tweet_id, use max_id and since_id.
        For more info: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
        :return: List
        '''
        replies=[]
        for tweet in tweepy.Cursor(self.api.search,q='to:'+user,since_id=sinceID, timeout=999999).items(maxID):
            #print(tweet)
            if hasattr(tweet, 'in_reply_to_status_id_str'):                                                                
                if (tweet.in_reply_to_status_id_str==tweet_id):
                    replies.append(tweet)
        return replies
