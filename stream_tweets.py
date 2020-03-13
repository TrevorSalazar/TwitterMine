from config import *
import tweepy
import sys

#streamlistener class inherits from streamlistener
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        is_retweet = False
        if hasattr(status, "retweeted_status"):
            is_retweet = True

        if hasattr(status, "extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text

        is_quote = hasattr(status, "quoted_status")
        quoted_text = ""
        if is_quote:
            if hasattr(status.quoted_status, "extended_tweet"):
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text

        remove_characters = [",","\n"]
        for c in remove_characters:
            text.replace(c," ")
            quoted_text.replace(c, " ")

        with open("out.csv", "a", encoding='utf-8') as f:
            f.write("%s,%s,%s,%s,%s,%s\n" % (status.created_at,status.user.screen_name,is_retweet,is_quote,text,quoted_text))
    
    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()

#Complete authorization and complete API endpoint
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Initialize streaming
streamListener = StreamListener()
stream = tweepy.Stream(auth=api.auth,listener=streamListener,tweet_mode='extended')

if __name__ == "__main__":
    #Complete auth and initialize API endpoint
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    #intialize stream
    streamlistener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamlistener, tweet_mode='extended')

    tags = ["ffxiv"]
    stream.filter(track=tags)
