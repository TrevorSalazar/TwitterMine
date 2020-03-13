import tweepy 
from config import *

  
# Function to extract tweets 
def get_tweets(username): 
          
        # Authorization to consumer key and consumer secret 
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  
        # Access to user's access key and access secret 
        auth.set_access_token(access_token, access_token_secret) 
  
        # Calling api 
        api = tweepy.API(auth) 
  
        # 200 tweets to be extracted 
        # number_of_tweets=200
        tweets = api.user_timeline(screen_name = username) 
  
        # Empty Array 
        # tmp=[]  
  
        # create array of tweet information: username,  
        # tweet id, date/time, text 
        # tweets_for_csv = [tweet.text for tweet in tweets] # CSV file created  
        for j in tweets: 
  
            # Appending tweets to the empty array tmp
            with open("user_tweets.csv", "a", encoding="utf-8") as f:
                f.write("%s,%s,%s\n" % (j.created_at,j.user.screen_name,j.text))
  
# Driver code 
if __name__ == '__main__': 
  
    # Here goes the twitter handle for the user 
    # whose tweets are to be extracted. 
    username = input("Enter a username: ")
    get_tweets(username)