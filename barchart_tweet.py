
from requests_oauthlib import OAuth1Session
import json
import matplotlib.pyplot as plt
import numpy as np
from config import *

#Set up auth, auth tokens
request_token_url = "https://api.twitter.com/oauth/request_token"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
fetch_response = oauth.fetch_request_token(request_token_url)
resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: {}".format(resource_owner_key))

# Get authorization
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: {}".format(authorization_url))
verifier = input("Paste the PIN here: ")

# Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

tweet_id = input("What Tweet ID do you want to look up? \n")
params = {"ids": tweet_id, "format": "detailed"}

response = oauth.get("https://api.twitter.com/labs/1/tweets", params=params)

# Turn respons into JSON
if response.encoding is None:
    response.encoding = "utf-8"
for data in response.iter_lines(decode_unicode=True):
    if data:
        jdata = json.loads(data)

print("Tweet text: ")
print(jdata["data"][0]["text"])
#print("Number of likes: ")
#print(jdata["data"][0]["stats"]["like_count"])
#print("Number of retweets: ")
#print(jdata["data"][0]["stats"]["retweet_count"])
#print("Reply count: ")
#print(jdata["data"][0]["stats"]["reply_count"])
#print("Quote count: ")
#print(jdata["data"][0]["stats"]["quote_count"])
print("Author ID: ")
print(jdata["data"][0]["author_id"])
print("Created At: ")
print(jdata["data"][0]["created_at"])

#Build plot, subplots
fig, ax = plt.subplots()
statistics = ('Likes', 'Retweets', 'Replies', 'Quotes')
y_pos = np.arange(len(statistics))
performance = (jdata["data"][0]["stats"]["like_count"], jdata["data"][0]["stats"]["retweet_count"],
    jdata["data"][0]["stats"]["reply_count"], jdata["data"][0]["stats"]["quote_count"])
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, statistics)

#Enumerate for subplots
for i, v in enumerate(performance):
    ax.text(i-.25, 
              v/performance[i]+100, 
              performance[i], 
              fontsize=14)

#Display Plot
plt.ylabel('Amount')
plt.xlabel('Metrics')
plt.title('Tweet Metric Data')
plt.show()