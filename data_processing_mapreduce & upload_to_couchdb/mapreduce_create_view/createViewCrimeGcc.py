import couchdb

design_doc = "groupGccTotalTweets"
mapFunc = '''function(doc) {
                if (doc.gcc) {
                    emit(doc.gcc, 1);
                }
            }'''

reduceFunc = '''function(keys, values) {
                return sum(values);
            }'''

couch = couchdb.Server("http://group6:123456@172.26.131.122:5984/")
db = couch["count_lang_tweet"]

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
