import tweepy 
from config import *
import matplotlib.pyplot as plt
import numpy as np
  
# Function to extract tweets 
def get_tweets(username): 
          
        # Authorization to consumer key and consumer secret 
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  
        # Access to user's access key and access secret 
        auth.set_access_token(access_token, access_token_secret) 
  
        # Calling api 
        api = tweepy.API(auth) 
  

        tweets = api.favorites(screen_name = username, count=500) 
  
        first_term = 0
        second_term = 0
        third_term = 0
        for j in tweets: 
            if("ffxiv" in j.text):
                first_term += 1

            if("coronavirus" in j.text):
                second_term += 1
            
            if("Sanders" in j.text):
                third_term += 1
            #with open("user_tweets.csv", "a", encoding="utf-8") as f:
                #f.write("%s,%s,%s\n" % (j.created_at,j.user.screen_name,j.text))
        
        labels = 'FFXIV', 'Coronavirus', 'Sanders'
        sizes = [first_term, second_term, third_term]
        colors = ['gold', 'lightcoral', 'blue']
        explode = (0, 0, 0)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

        plt.axis('equal')
        plt.show()
  
# Driver code 
if __name__ == '__main__': 
  
    # Here goes the twitter handle for the user 
    # whose likes are to be extracted. 
    username = input("Enter a username: ")
    get_tweets(username)