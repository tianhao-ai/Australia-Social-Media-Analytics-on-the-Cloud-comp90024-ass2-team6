from mastodon import Mastodon, StreamListener
import requests
import json
import os
import re
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk import download

m = Mastodon(
    api_base_url = f'https://aus.social',
    access_token = 'F8xDj5tGzeUoTt-mYEaeMICsQ4BGsFdOY4lBfr5D4rQ'
)

# Download required NLTK data
download('punkt')
download('stopwords')


def count_word(text):
    # Clean text: remove special characters, numbers, and convert to lowercase
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text).lower()

    # Tokenize the text
    tokens = word_tokenize(cleaned_text)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    punkt = set(stopwords.words("english"))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return filtered_tokens

def upload_to_couchdb(db_url, dbname, doc):
    response = requests.post(f"{db_url}/{dbname}", json=doc)
    if response.status_code not in (201, 202):
        print(f"Failed to upload document: {doc}")
        print(f"Response: {response.status_code}, {response.text}")

class Listener(StreamListener):
    def __init__(self):
        super(Listener, self).__init__()

    def on_update(self, status):

        obj = json.loads(json.dumps(status, indent=2, sort_keys=True, default=str))
        soup = BeautifulSoup(obj['content'], "html.parser")

        # Extract text
        text = soup.get_text(separator=" ")

        # Extract links
        links = [a["href"] for a in soup.find_all("a", href=True)]

        # Extract hashtags
        hashtags = [hashtag.text for hashtag in soup.find_all("span", class_="span")]

        # Extract mentions
        mentions = [mention.text for mention in soup.find_all("span", class_="h-card")]
        obj["extracted_text"] = text
        obj["extracted_links"] = links
        obj["extracted_hashtags"] = hashtags
        obj["extracted_mentions"] = mentions
        tokens = count_word(text)
        obj['extracted_tokens'] = tokens
        upload_to_couchdb("http://group6:123456@172.26.133.72:5984", "aus_social_tweet", obj)
        print('tokens: ',tokens)
        

# Set the desired timeout value (in seconds)
m.stream_public(Listener())