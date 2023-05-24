import couchdb
import json
username='group6'
passwd = '123456'
ip = '172.26.131.122'
hostName='http://{}:{}@{}:5984/'.format(username, passwd, ip)
couch = couchdb.Server(hostName)

def writeToCouchdb(databaseName, jsonName):
    # Connect to CouchDB
    # Create the database if it doesn't exist
    if databaseName not in couch:
        couch.create(databaseName)

    # Get the database
    db = couch[databaseName]

    # Write the documents to the database
    with open(jsonName, 'r') as f:
        for line in f:
            records = json.loads(line)
            for element in records:
                db.save(element)
                
writeToCouchdb('sudo_gcc_educationlevel', '../graph_data/EducationLevel_SUDO_after cleaning.json')