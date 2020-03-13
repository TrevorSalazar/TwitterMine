import tweepy
from config import *
import matplotlib.pyplot as plt
import numpy as np
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

username = input("Pick a user to retrieve tweets from: ")
i = 0
retweets = 0
daily_tweets = []
tweets_today = 0
current_day = ""
first_day = ""
last_day = ""
for status in tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode="extended").items():
    #with open("%s.csv" % username, "a", encoding="utf-8") as f:
        #f.write("%s,%s,%s\n" % (status.created_at,status.user.screen_name,status.full_text))
    i += 1
    if(len(daily_tweets) == 0):
        first_day = status.created_at
    if("RT" in status.full_text):
        retweets += 1
    if(current_day != str(status.created_at)[0:10]):
        daily_tweets.append(tweets_today)
        tweets_today = 0
        current_day = str(status.created_at)[0:10]
        last_day = status.created_at
    
    tweets_today += 1


print("Statistics!")
print("Number of tweets retrieved: ")
print(i)
print("Percentage of Tweets which were retweets: ")
print(retweets / i)
print("Days catalogued: ")
print(len(daily_tweets))
print("Average tweets on days that user DID tweet per day: ")
print(sum(daily_tweets) / len(daily_tweets))
print("Average tweets per day overall: ")
print(sum(daily_tweets) / ((first_day - last_day).days + 2))
labels = 'Regular tweets', 'Retweets'
sizes = [i - retweets, retweets]
colors = ['gold', 'lightcoral']
explode = (0.1, 0)
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.show()

statistics = ('Avg Tweets/day', 'Avg Tweets/day on days that user DID Tweet')
y_pos = np.arange(len(statistics))
performance = ((sum(daily_tweets) / ((first_day - last_day).days + 2)), (sum(daily_tweets) / len(daily_tweets)))
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, statistics)
plt.ylabel('Number of tweets')
plt.title('Average Tweets Comparison')
plt.show()