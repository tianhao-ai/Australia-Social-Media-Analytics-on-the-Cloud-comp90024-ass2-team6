import couchdb
import json
username='group6'
passwd = '123456'
ip = '172.26.131.122'
hostName='http://{}:{}@{}:5984/'.format(username, passwd, ip)
couch = couchdb.Server(hostName)

db = couch['bad_lang_tweet']

design_doc="whatbad"
def mapreduce(db):
    mapFunc = '''function(doc) {
                emit([doc.gcc, doc.bad_word], 1);
    }'''
    reduceFunc = 'function(keys, values) { return sum(values); }'
    ddoc = {
        "_id": "_design/{}".format(design_doc),
        "views": {
            "my_view": {
                "map": mapFunc,
                "reduce": reduceFunc
            }
        }
    }
    db.save(ddoc)
mapreduce(db)
import requests

url = "http://172.26.131.122:5984/bad_lang_tweet/_design/whatbad/_view/my_view?group=true"
username = "group6"
password = "123456"

response = requests.get(url, auth=(username, password))

if response.status_code != 200:
    print(f"Error: {response.status_code}")
    
file_name = "count_gcc_lang_bad.json"

# Write the JSON object to a file
with open(file_name, "w") as file:
    json.dump(data, file, indent=4)
    