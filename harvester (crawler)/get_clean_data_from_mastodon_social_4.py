from mastodon import Mastodon, StreamListener
import requests
import json
import os
import re
from bs4 import BeautifulSoup
from better_profanity import profanity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import download
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

m = Mastodon(
    api_base_url = f'https://mastodon.social',
    access_token = 'yGUk6yJ3mHDN5vZUUmxiVRx7XOnP_hDZ-PHycJOKBSg'
)


# Download required NLTK data
download('punkt')
download('stopwords')
download('averaged_perceptron_tagger')
download('wordnet')

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

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
def detect_crime(tokenized_text):
    crime_keywords = [
    'crime', 'felony', 'misdemeanor', 'offense', 'violation',
    'assault',  'homicide', 'manslaughter', 'murder',
    'rape', 'harassment', 'stalking',
    'kidnapping', 'abduction', 'imprisonment',
    'robbery', 'burglary', 'theft', 'larceny', 'shoplifting', 'embezzlement', 'fraud',
    'arson', 'vandalism', 'mischief', 'trespass',
    'drug', 'narcotics',
    'DUI', 'DWI',
    'extortion', 'blackmail', 'bribery', 'corruption', 'racketeering',
    'terrorism', 'cybercrime', 'hacking', 'phishing',
    'trafficking', 'prostitution', 'pimping', 'pandering', 'solicitation',
    'counterfeiting', 'forgery',
    'perjury'
    ]
    lemmatizer = WordNetLemmatizer()

    pos_tags = nltk.pos_tag(tokenized_text)

    # Get appropriate POS tag for lemmatization
    lemmatized_tokens = [lemmatizer.lemmatize(token.lower(), get_wordnet_pos(pos)) for token, pos in pos_tags]

    # If any of the lemmatized tokens is in crime_keywords, return True. Else, return False.
    return any(token in crime_keywords for token in lemmatized_tokens)


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

        tokens = count_word(text)
        tokens_user_name = count_word(obj['account']['username'])
        tokens_display_name = count_word(obj['account']['display_name'])
        
        
        # Create a new object with the extracted data
        new_obj = {
            "original_text":text,
            "extracted_text": text,
            "extracted_links": links,
            "extracted_hashtags": hashtags,
            "extracted_mentions": mentions,
            "extracted_tokens": tokens,
            "discoverable":obj['account']['discoverable'],
            "followers_count":obj['account']['followers_count'],
            "following_count":obj['account']['following_count'],
            "bot":obj['account']['bot'],
            "language":obj['language'],
            "visibility":obj['visibility'],
            "sensitive":obj['sensitive'],
            "crime_in_username":detect_crime(tokens_user_name),
            "crime_in_displayname":detect_crime(tokens_display_name),
            "crime_in_text":detect_crime(tokens),
            "vulgar_in_username":profanity.contains_profanity(obj['account']['username']),
            "vulgar_in_displayname":profanity.contains_profanity(obj['account']['display_name']),
            "vulgar_in_text":profanity.contains_profanity(text)
        }
        upload_to_couchdb("http://group6:123456@172.26.128.73:5984", "mastodon_social_clean", new_obj)
        

m.stream_public(Listener())