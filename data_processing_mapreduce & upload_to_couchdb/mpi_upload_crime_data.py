import re
import json
import requests
from mpi4py import MPI
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

'''
# download this if you not have this package
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
'''

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

# Define a list of crime-related keywords
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
global_crime_keyword_counts = {keyword:0 for keyword in crime_keywords} # use for test

def count_keywords(tokenized_text, keywords):
    lemmatizer = WordNetLemmatizer()

    tokens = tokenized_text.lower().split('|')
    pos_tags = nltk.pos_tag(tokens)
    # 
    lemmatized_tokens = [lemmatizer.lemmatize(token, get_wordnet_pos(pos)) for token, pos in pos_tags]

    crime_related_keywords = [token for token in lemmatized_tokens if token in keywords]

    return crime_related_keywords

def gccOfTweet(fullName, sal):
    city = fullName.split(", ")[0].lower()  # get city name
    if city in sal:
        gcc_before = sal[city]["gcc"]
        # use regular expression to check for rural
        if re.sub("[0-9]", "", gcc_before)[0] != "r":
            return gcc_before
    return None

def upload_to_couchdb(db_url, doc):
    response = requests.post(f'{db_url}/crime_lang_tweet', json=doc)
    if response.status_code not in (201, 202):
        print(f"Failed to upload document: {doc}")
        print(f"Response: {response.status_code}, {response.text}")

def countGeoLang(jsonFile, db_url, rank, size):
    with open("sal.json", "r") as f:
        sal = json.load(f)

    index = 0
    noplaceId = 0
    dictGccFullNames = {
        "1gsyd": "Greater Sydney",
        "2gmel": "Greater Melbourne",
        "3gbri": "Greater Brisbane",
        "4gade": "Greater Adelaide",
        "5gper": "Greater Perth",
        "6ghob": "Greater Hobart",
        "7gdar": "Greater Darwin",
        "8acte": "Australian Capital Territory (Canberra)",
        "9oter": "Other Territory",
    }

    with open(jsonFile, 'r', encoding='utf-8') as file:
        for line_index, line in enumerate(file):
            if line_index % size != rank:
                continue
            index += 1
            if index % 500000 == 0:
                print("parse tweets lines: {}, noplaceid = {}".format(index, noplaceId))
                print(global_crime_keyword_counts)

            element = json.loads(line.strip(',\n'))
            geo = element['doc']['data'].get('geo', {})
            if len(geo) != 0:
                if 'place_id' not in geo.keys():
                    noplaceId += 1
                    continue
                try:
                    includes = element['doc']['includes']
                    if isinstance(includes, list) and len(includes) > 0 and 'full_name' in includes[0]:
                        fullName = includes[0]['full_name']
                    elif isinstance(includes, dict) and 'places' in includes and len(includes['places']) > 0 and 'full_name' in includes['places'][0]:
                        fullName = includes['places'][0]['full_name']
                except (IndexError, KeyError, TypeError):
                    continue
                gcc = gccOfTweet(fullName, sal)
                if gcc is None:
                    continue
                element['gcc'] = dictGccFullNames[gcc]

                # Check if the tweet contains crime-related keywords
                tokens = element['value']['tokens']
                keyword_counts = count_keywords(tokens, crime_keywords)

                # Only upload the tweet if it contains at least one crime-related keyword
                if len(keyword_counts) > 0:
                    # Add the keyword frequency to the element
                    element['crime_keyword_counts'] = keyword_counts
                    for keyword in keyword_counts:
                        global_crime_keyword_counts[keyword] += 1
                    #Upload the element to CouchDB
                    upload_to_couchdb(db_url, element)

if __name__ == "__main__":
    db_url = "http://group6:123456@172.26.131.122:5984"
    jsonFile = "contain_geo_tweet.json"

    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    countGeoLang(jsonFile, db_url, rank, size)