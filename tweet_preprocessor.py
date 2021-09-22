# tweet_preprocessor.py


'''
@author: Souvik Das
Institute: University at Buffalo
'''

import demoji, re, datetime
import preprocessor as p


# demoji.download_codes()


class TWPreprocessor:
    @classmethod
    def preprocess(cls, tweet,country):
        '''
        Do tweet pre-processing before indexing, make sure all the field data types are in the format as asked in the project doc.
        :param tweet:
        :return: dict
        '''

        preprocess_tweet={}
        preprocess_tweet['id'] = tweet.id
        preprocess_tweet['tweet_text'] = tweet.text
        preprocess_tweet['tweet_date'] = _get_tweet_date(tweet._json['created_at'])
        preprocess_tweet['poi_id'] = tweet.user.id
        preprocess_tweet['poi_name'] = tweet.user.name
        cleaned_text = _text_cleaner(tweet.text.split(' ', 1)[1])[0]
        preprocess_tweet['country'] = country
        if tweet.lang == 'en':
                preprocess_tweet['tweet_lang']='en'
                preprocess_tweet['text_en'] = cleaned_text
            elif(tweet.lang == 'hi'):
                preprocess_tweet['tweet_lang']='hi'
                preprocess_tweet['text_hi'] = cleaned_text
            elif(tweet.lang == 'es'):
                preprocess_tweet['tweet_lang']='es'
                preprocess_tweet['text_es'] = cleaned_text
        preprocess_tweet['replied_to_tweet_id'] = tweet.in_reply_to_status_id_str
        preprocess_tweet['replied_to_user_id']= tweet.in_reply_to_user_id_str
        if tweet.in_reply_to_status_id_str != None:
            preprocess_tweet['reply_text'] = tweet.text
        preprocess_tweet['hashtags'] = _get_entities(tweet,type='hashtags')
        preprocess_tweet['mentions'] = _get_entities(tweet,type='mentions')
        preprocess_tweet['tweet_urls'] = _get_entities(tweet,type='urls')
        preprocess_tweet['tweet_emoticons'] = _text_cleaner(tweet.text.split(' ', 1)[1])[1]
     
        return preprocess_tweet

        



def _get_entities(tweet, type=None):
    result = []
    if type == 'hashtags':
        hashtags = tweet.entities['hashtags']

        for hashtag in hashtags:
            result.append(hashtag['text'])
    elif type == 'mentions':
        mentions = tweet.entities['user_mentions']

        for mention in mentions:
            result.append(mention['screen_name'])
    elif type == 'urls':
        urls = tweet['entities']['urls']

        for url in urls:
            result.append(url['url'])

    return result


def _text_cleaner(text):
    emoticons_happy = list([
        ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
        ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
        '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
        'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
        '<3'
    ])
    emoticons_sad = list([
        ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
        ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
        ':c', ':{', '>:\\', ';('
    ])
    all_emoticons = emoticons_happy + emoticons_sad
    emojis = list(demoji.findall(text).keys())
    clean_text = demoji.replace(text, '')

    for emo in all_emoticons:
        if (emo in clean_text):
            clean_text = clean_text.replace(emo, '')
            emojis.append(emo)

    clean_text = p.clean(text)
    # preprocessor.set_options(preprocessor.OPT.EMOJI, preprocessor.OPT.SMILEY)
    # emojis= preprocessor.parse(text)

    return clean_text, emojis


def _get_tweet_date(tweet_date):
    return datetime.datetime.strftime(_hour_rounder(datetime.datetime.strptime(str(tweet_date), '%a %b %d %H:%M:%S +0000 %Y')),"%Y-%m-%dT%H:%M:%SZ")

def _hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour))\
            + datetime.timedelta(hours=t.minute // 30)