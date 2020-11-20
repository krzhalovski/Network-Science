import json
import os
from . import utils

class Representative():
    
    def __init__(self, state, chamber_of_congress, name, party, screen_name):
        self.state = state
        self.chamber_of_congress = chamber_of_congress
        self.name = name
        self.screen_name = screen_name
        self.party = party
        
        self.is_parsed = False
        self.retweets = []
        self.mentions = []
        self.hashtags = []
        self.likes = []
        
        self.image = None
        self.number_of_tweets = 0
        
    def parse_user(self, directory):
        if self.is_parsed:
            return None
        
        path = directory+self.screen_name+'/'
        files = os.listdir(directory + self.screen_name)
        
        self.number_of_tweets = len(files)
        
        for tweet_id in files:
            with open(path+tweet_id) as tw:
                tweet = json.load(tw)
            
            if self.image == None:
                self.image = tweet['user']['profile_image_url_https']
            is_retweet, hashtags, mentions = utils.get_tweet_info(tweet)
        
            if is_retweet:
                self.retweets.append(tweet['retweeted_status']['user']['screen_name'])

            else:
                self.hashtags.extend(hashtags)
                self.mentions.extend(mentions)
                
        self.hashtags = [hashtag.lower() for hashtag in self.hashtags]
        self.is_parsed = True
    
    def update_likes(self, likes):
        self.likes = likes
        
    def get_retweet_percentage(self):
        return len(self.retweets)/float(self.number_of_tweets)
    
    def __str__(self):
        return f'{"Republican" if self.party=="R" else "Democrat"} {self.chamber_of_congress} {self.name} of {self.state}'
    
    def __dict__(self):
        return {
            'state': self.state,
            'chamber_of_congress': self.chamber_of_congress,
            'name': self.name,
            'screen_name': self.screen_name,
            'party': self.party,
            'image': self.image,
        }
            
            