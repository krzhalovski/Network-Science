import tweepy
import json
import os

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

def parse_user(user_directory_path):
    ids = os.listdir(user_directory_path)
    
    retweeted_users = []
    user_hashtags = []
    user_mentions = []
    
    for _id in ids:
        full_path = user_directory_path + _id
        
        with open(full_path, 'r') as f:
            tweet = json.load(f)
            
        is_retweet, hashtags, mentions = get_tweet_info(tweet)
        
        if is_retweet:
            retweeted_users.append(tweet['retweeted_status']['user']['screen_name'])
        
        else:
            user_hashtags.extend(hashtags)
            user_mentions.extend(mentions)
        
    return retweeted_users, user_hashtags, user_mentions
        
        
    