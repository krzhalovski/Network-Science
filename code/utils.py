import tweepy
import json
import os
import requests

from collections import defaultdict
from tqdm import tqdm

def load_credentials(file):
    with open(file) as f:
        return json.load(f)
    
def setup_tweepy(credentials):
    auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
    auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
    api = tweepy.API(auth)
    
    return auth, api

def get_user_tweets(api, user, count=500):
    tweets = []
    
    for tweet in tweepy.Cursor(api.user_timeline, wait_on_rate_limit=True, id=user, tweet_mode='extended').items(count):
        tweets.append(tweet)
        
    return tweets

def get_user_likes(api, user, count=200):
    return api.favorites(user, count=count, wait_on_rate_limit=True, tweet_mode='extended')

def get_tweet_info(tweet):
    is_retweet = 'retweeted_status' in tweet.keys()
    
    hashtags = [entity['text'] for entity in tweet['entities']['hashtags']]
    user_mentions = [entity['screen_name'] for entity in tweet['entities']['user_mentions']]
    
    return (is_retweet, hashtags, user_mentions)

def get_user_picture(party_directory, path_to_save):
    for user in tqdm(os.listdir(party_directory)):
        if user.startswith('.') or len(os.listdir(party_directory+user)) == 0:
            continue
        
        sample_tweet_id = os.listdir(party_directory+user)[0]
        with open(party_directory+user+'/'+sample_tweet_id) as f:
            sample_tweet = json.load(f)
        
        r = requests.get(sample_tweet['user']['profile_image_url_https'], stream=True)

        if r.status_code == 200:
            with open(f'{path_to_save}{user}.jpg', 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        
def get_hashtag_corpus(representatives):
    corpus = defaultdict(int)

    for rep in representatives:
        for hashtag in rep.hashtags:
            corpus[hashtag] += 1
            
    return corpus
    