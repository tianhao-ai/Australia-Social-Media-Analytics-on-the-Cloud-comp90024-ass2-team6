# Choosing and upload the bad word tweet
import re
import json
import requests
from mpi4py import MPI
import pandas as pd

# process finding all the bad word
# which we choose the bad words which returned by mapreduce, and we just considered the bad words from top five tweet languages
# which is en,in,es,ja,zh
# which is English, Hindi, Spanish, Japanese, Chinese
bad_word_all = []
# Bad words in Hindi
hindi= 'आंड़,आंड,आँड,बहनचोद,बेहेनचोद,भेनचोद,बकचोद,बकचोदी,बेवड़ा,बेवड़े,बेवकूफ,भड़ुआ,भड़वा,भोसड़ा,भोसड़ीके,भोसड़ीकी,भोसड़ीवाला,भोसड़ीवाले,बब्बे,बूबे,बुर,चरसी,चूचे,चूची,चुची,चोद,चुदने,चुदवा,चुदवाने,चाट,चूत,चूतिया,चुटिया,दलाल,दलले,फट्टू,गधा,गधे,गधालंड,गांड,गांडू,गंडफट,गंडिया,गंडिये,गू,गोटे,हग,हग्गू,हगने,हरामी,हरामजादा,हरामज़ादा,हरामजादे,हरामज़ादे,हरामखोर,झाट,झाटू,कुत्ता,कुत्ते,कुतिया,कुत्ती,लेंडी,लोड़े,लौड़े,लौड़ा,लोड़ा,लौडा,लिंग,लोडा,लोडे,लंड,लौंडा,लौंडे,लौंडी,लौंडिया,लुल्ली,मार,मारो,मारूंगा,मादरचोद,मादरचूत,मादरचुत,मम्मे,मूत,मुत,मूतने,मुतने,मूठ,मुठ,नुननी,नुननु,पाजी,पेसाब,पेशाब,पिल्ला,पिल्ले,पिसाब,पोरकिस्तान,रांड,रंडी,सुअर,सूअर,टट्टे,टट्टी,उल्लू'
bad_words_hindi = []
for word in hindi.split(','):
    bad_words_hindi.append(word)

# Bad words in English
bad_words_eng = []
all_eng = pd.read_csv('../graph_data/bad_word/en.csv')
for value in all_eng['2g1c']:
    bad_words_eng.append(value)

# Bad words in Spanish
bad_words_es = []
all_es = pd.read_csv('../graph_data/bad_word/es.csv')
for value in all_es['Asesinato']:
    bad_words_es.append(value)
bad_words_es

# Bad words in Japanese
bad_words_ja = []
all_ja = pd.read_csv('../graph_data/bad_word/ja.csv')
for value in all_ja['3p']:
    bad_words_ja.append(value)
bad_words_ja

# Bad words in Chinese
bad_words_zh = []
all_zh = pd.read_csv('../graph_data/bad_word/zh.csv')
for value in all_zh['13.']:
    bad_words_zh.append(value)
bad_words_zh

bad_words_all = bad_words_eng + bad_words_es + bad_words_ja + bad_words_hindi + bad_words_zh
def gccOfTweet(fullName, sal):
    city = fullName.split(", ")[0].lower()  # get city name
    if city in sal:
        gcc_before = sal[city]["gcc"]
        # use regular expression to check for rural
        if re.sub("[0-9]", "", gcc_before)[0] != "r":
            return gcc_before
    return None

def upload_to_couchdb(db_url, doc):
    response = requests.post(f'{db_url}/bad_lang_tweet', json=doc)
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
            if index % 100000 == 0:
                print("parse tweets lines: {}, noplaceid = {}".format(index, noplaceId))

            element = json.loads(line.strip(',\n'))
            geo = element['doc']['data'].get('geo', {})
            # get the word which after preprocessing into a list
            # if there is no tokens included
            word = element['value']['tokens'].split('|')
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
                    print(f"Error occurred in element: {element}")
                    continue
                gcc = gccOfTweet(fullName, sal)
                if gcc is None:
                    continue
                element['gcc'] = dictGccFullNames[gcc]
                # upload the element to CouchDB
                for small_word in word:
                    if small_word in bad_words_all:
                        element['bad_word'] = small_word
                        upload_to_couchdb(db_url, element)

if __name__ == "__main__":
    db_url = "http://group6:123456@172.26.131.122:5984"
    jsonFile = "contain_geo_tweet.json"
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    countGeoLang(jsonFile, db_url, rank, size)




