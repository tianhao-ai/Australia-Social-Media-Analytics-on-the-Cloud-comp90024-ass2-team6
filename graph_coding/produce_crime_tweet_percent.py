import requests
import json

# Replace the URL, username, password, and database_name with your own
url = "http://group6:123456@172.26.131.122:5984/count_lang_tweet/_design/groupGccTotalTweets/_view/my_view?group_level=1"

response = requests.get(url)
view_data = response.json()

gcc_total_tweet_counts = {}
for row in view_data["rows"]:
    gcc_name = row["key"]
    tweet_count = row["value"]
    gcc_total_tweet_counts[gcc_name] = tweet_count
# Replace the URL, username, password, and database_name with your own
url = "http://group6:123456@172.26.131.122:5984/crime_lang_tweet/_design/groupGccTotalTweets/_view/my_view?group_level=1"

response = requests.get(url)
view_data = response.json()

gcc_keyword_counts = {}
for row in view_data["rows"]:
    gcc_name = row["key"]
    keyword_counts = row["value"]
    gcc_keyword_counts[gcc_name] = keyword_counts

# Print the result
print(json.dumps(gcc_keyword_counts, indent=4))
percentage_dict = {}
for gcc_name in gcc_keyword_counts:
    keyword_count = gcc_keyword_counts[gcc_name]
    total_count = gcc_total_tweet_counts[gcc_name]
    percentage = (keyword_count / total_count) * 100
    percentage_dict[gcc_name] = percentage

# Print the result
print(json.dumps(percentage_dict, indent=4))

with open('../graph_data/percentTweetCrime.json', 'w') as json_file:
    json.dump(percentage_dict, json_file, indent=4)
