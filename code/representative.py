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
        
    def parse_user(self, directory):
        if self.is_parsed:
            return None
        
        path = directory+self.screen_name+'/'
        
        for tweet_id in os.listdir(directory + self.screen_name):
            with open(path+tweet_id) as tw:
                tweet = json.load(tw)
            
            is_retweet, hashtags, mentions = utils.get_tweet_info(tweet)
        
            if is_retweet:
                self.retweets.append(tweet['retweeted_status']['user']['screen_name'])

            else:
                self.hashtags.extend(hashtags)
                self.mentions.extend(mentions)
        
        self.hashtags = [hashtag.lower() for hashtag in self.hashtags]
    
    def update_likes(self, likes):
        self.likes = likes
    
    def __str__(self):
        return f'{"Republican" if self.party=="R" else "Democrat"} {self.chamber_of_congress} {self.name} of {self.state}'
    
    def __repr__(self):
        return (self.name, self.screen_name, self.state, self.chamber_of_congress)
            
            