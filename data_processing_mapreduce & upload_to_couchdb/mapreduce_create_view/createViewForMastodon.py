import couchdb

mastodon_url = 
["http://group6:123456@172.26.133.72:5984/","http://group6:123456@172.26.128.73:5984/"]
analysis_feature = 
["bot","language","sensitive","crime_in_text","vulgar_in_text"]

# Function to create a design document for a given feature
def create_view(feature):
    design_doc = "group"+feature

    # Map function
    mapFunc = f'''function(doc) {{
                    if (doc.{feature} !== undefined) {{
                        emit(doc.{feature}, 1);
                    }}
                }}'''

    # Reduce function
    reduceFunc = '''function(keys, values, rereduce) {
                    if (rereduce) {
                        return sum(values);
                    }
                    return values.length;
                }'''

    return {
        "_id": "_design/{}".format(design_doc),
        "views": {
            "my_view": {
                "map": mapFunc,
                "reduce": reduceFunc
            }
        }
    }

# Iterate over each URL and feature
for i,url in enumerate(mastodon_url):
    # Replace the URL, username, and password with your own CouchDB 
credentials
    couch = couchdb.Server(url)
    if i == 1:
        db = couch["mastodon_social_clean"]
    else:
        db = couch["aus_social_tweet_clean"]
    for feature in analysis_feature:
        view = create_view(feature)
        db.save(view)
