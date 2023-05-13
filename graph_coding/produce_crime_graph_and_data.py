import requests
import json
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
# Replace the URL, username, password with your own config
url = "http://group6:123456@172.26.131.122:5984/crime_lang_tweet/_design/groupGccCrimeKeywordsTotal/_view/my_view?group_level=1"

response = requests.get(url)
view_data = response.json()

gcc_keyword_counts = {}
for row in view_data["rows"]:
    gcc_name = row["key"]
    keyword_counts = row["value"]
    gcc_keyword_counts[gcc_name] = keyword_counts

# Print the result
print(json.dumps(gcc_keyword_counts, indent=4))
with open('../graph_data/tweetContainCrimeGcc.json', 'w') as json_file:
    json.dump(gcc_keyword_counts, json_file, indent=4)
url = "http://group6:123456@172.26.131.122:5984/crime_lang_tweet/_design/groupGccCrimeKeywordsRank/_view/my_view?group_level=1"

response = requests.get(url)
view_data = response.json()

gcc_keyword_counts = {}
for row in view_data["rows"]:
    gcc_name = row["key"]
    keyword_counts = row["value"]
    gcc_keyword_counts[gcc_name] = keyword_counts

# Print the result
print(json.dumps(gcc_keyword_counts, indent=4))
with open('../graph_data/eachCrimeKeywordGcc.json', 'w') as json_file:
    json.dump(gcc_keyword_counts, json_file, indent=4)
# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame(gcc_keyword_counts)

df = df.drop('crime',errors='ignore')
# Convert counts to percentages
df = df.apply(lambda x: x / x.sum() * 100, axis=0)

# Keep only the top 10 keywords by count for each region
df = df.apply(lambda x: x.nlargest(10), axis=0)

df = df.fillna(0)
# Plot a heatmap
plt.figure(figsize=(15, 10))
sns.heatmap(df, cmap='viridis')
plt.title('Top 10 Crime Keywords by Region (Percentage)')
plt.xlabel('Regions')
plt.ylabel('Keywords')

# Rotate x-axis labels for better visibility
plt.xticks(rotation=45, ha='right')
# Save the figure
plt.savefig('../Graph/top10_crime_keyword.png')

plt.show()
