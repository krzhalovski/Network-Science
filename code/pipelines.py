from . import utils
import json
import os
from tqdm import tqdm

def like_pipeline(api, list_of_users):
    """
    Returns a list of authors of liked tweets for each user,
    along with a list of users for which a failed retrieve occured.
    """
    
    likes = {}
    failed = []
    
    for user in tqdm(list_of_users):
        try:
            liked_tweets = utils.get_user_likes(api, user)
            screen_names = [like._json['user']['screen_name'] for like in liked_tweets]
            likes[user] = screen_names
        except Exception as e:
            failed.append((user, e))
            
    return likes, failed

def tweet_pipeline(api, list_of_users, directory_path):
    """
    Saves tweets for a list of users in the specified directory
    """
    tweets = []
    failed = []
    
    for user in tqdm(list_of_users):
        try:
            tweets = utils.get_user_tweets(api, user)
            os.makedirs(f'{directory_path}{user}/')
            
            for tweet in tweets:
                tweet_id = tweet._json['id_str']
                
                with open(f'{directory_path}{user}/{tweet_id}.json', 'w') as f:
                    f.truncate()
                    json.dump(tweet._json, f)
                    f.close()
                    
        except Exception as e:
            failed.append((user, e))
    
    return failed
            