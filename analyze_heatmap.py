import pandas as pd
from collections import Counter
import ast

tweets = pd.read_csv("saved_tweets.csv")

print (tweets)

# Extract hashtags and put them in a list

list_hashtag_strings = [entry for entry in tweets.hashtags]
list_hashtag_lists = ast.literal_eval(','.join(list_hashtag_strings))
hashtag_list = [ht.lower() for list_ in list_hashtag_lists for ht in list_]

# Count most common hashtags
counter_hashtags = Counter(hashtag_list)
counter_hashtags.most_common(20)

from geopy.geocoders import Nominatim
import gmplot

geolocator = Nominatim()

# Go through all tweets and add locations to 'coordinates' dictionary
coordinates = {'latitude': [], 'longitude': []}
for count, user_loc in enumerate(tweets.location):
    try:
        location = geolocator.geocode(user_loc)
        
        # If coordinates are found for location
        if location:
            coordinates['latitude'].append(location.latitude)
            coordinates['longitude'].append(location.longitude)
            
    # If too many connection requests
    except:
        pass
    
# Instantiate and center a GoogleMapPlotter object to show our map
gmap = gmplot.GoogleMapPlotter(30, 0, 3)

# Insert points on the map passing a list of latitudes and longitudes
gmap.heatmap(coordinates['latitude'], coordinates['longitude'], radius=20)

# Save the map to html file
gmap.draw("ffxiv_heatmap.html")