import requests
import json
import pandas as pd

analysis_feature =  ["groupbot","groupsensitive","groupcrime_in_text","groupvulgar_in_text"]
results = {}
servers = ['mastodon_social','aus_social']
for i,server in enumerate(servers): 
    for features in analysis_feature:
        if i == 0 :
            url = f"http://group6:123456@172.26.128.73:5984/mastodon_social_clean/_design/{features}/_view/my_view?group_level=1"
        else:
            url = f"http://group6:123456@172.26.133.72:5984/aus_social_tweet_clean/_design/{features}/_view/my_view?group_level=1"
        
        response = requests.get(url)
        response.raise_for_status()  # Raises a HTTPError if the response was unsuccessful
        view_data = response.json()
        for row in view_data["rows"]:
            gcc_name = row["key"]
            keyword_counts = row["value"]
            if gcc_name == True:
                # Calculate the percentage of 'true' values and store it in the results dictionary
                results[(server, features)] = keyword_counts / (view_data['rows'][0]['value'] + view_data['rows'][1]['value']) * 100
                
df = pd.DataFrame(list(results.items()), columns=['Server_Feature', 
'Percentage'])
df['Server'], df['Feature'] = zip(*df['Server_Feature'])
df = df.drop(columns='Server_Feature')

# Reorder the columns
df = df[['Server', 'Feature', 'Percentage']]

# Pivot the DataFrame
df_pivot = df.pivot(index='Feature', columns='Server', values='Percentage')

# Rename the index
df_pivot.index = ['Bot detected percentage', 'Sensitive detected percentage', 'Crime in text detected percentage', 'Vulgar in text detected percentage']

# Show the pivoted DataFrame
print(df_pivot)
for index, row in df_pivot.iterrows():
    # Create a new DataFrame for each row
    df_row = pd.DataFrame(row).transpose()

    # Use the row name (index) to create a unique filename for each CSV
    filename = index.replace(' ', '_') + '.csv' # replaces spaces with underscores

    # Save the DataFrame to a CSV file
    df_row.to_csv(f'../graph_data/{filename}', index=True, header=True)
import matplotlib.pyplot as plt

# Loop through servers
servers = ['mastodon_social','aus_social']
for i, server in enumerate(servers):
    if i == 0 :
        url = f"http://group6:123456@172.26.128.73:5984/mastodon_social_clean/_design/grouplanguage/_view/my_view?group_level=1"
    else:
        url = f"http://group6:123456@172.26.133.72:5984/aus_social_tweet_clean/_design/grouplanguage/_view/my_view?group_level=1"
    
    response = requests.get(url)
    response.raise_for_status()  # Raises a HTTPError if the response was unsuccessful
    view_data = response.json()

    # Create a dictionary to store languages and their counts
    language_counts = {}
    for row in view_data["rows"]:
        language = row["key"]
        count = row["value"]
        language_counts[language] = count

    # Convert the dictionary to a DataFrame and sort by count
    df_language = pd.DataFrame(list(language_counts.items()), columns=['Language', 'Count'])
    df_language = df_language.sort_values(by='Count', ascending=False)
    
    # Select the top 5 languages
    df_top5 = df_language.iloc[:5]
    
    # Save the DataFrame to a CSV file
    df_top5.to_csv(f'../graph_data/{server}_top5_languages.csv', index=False)

    # Plot a pie chart
    plt.figure(figsize=(6,6))
    plt.pie(df_top5['Count'], labels=df_top5['Language'], autopct='%1.1f%%')
    plt.title(f'Top 5 languages in {server}')
    plt.show()
