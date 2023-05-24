import couchdb
design_doc = "groupGccCrimeKeywordsTotal"
mapFunc = '''function(doc) {
                if (doc.gcc && doc.crime_keyword_counts) {
                    doc.crime_keyword_counts.forEach(function(keyword) {
                        emit(doc.gcc, {keyword: 1});
                    });
                }
            }'''

reduceFunc = '''function(keys, values) {
                var result = {};
                values.forEach(function(value) {
                    for (var keyword in value) {
                        if (!result[keyword]) {
                            result[keyword] = 0;
                        }
                        result[keyword] += value[keyword];
                    }
                });
                return result;
            }'''
couch = couchdb.Server("http://group6:123456@172.26.131.122:5984/")
db = couch["crime_lang_tweet"]

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
# Start to create second view
design_doc = "groupGccCrimeKeywordsRank"
mapFunc = '''function(doc) {
                if (doc.gcc && doc.crime_keyword_counts) {
                    var keyword_counts = {};
                    doc.crime_keyword_counts.forEach(function(keyword) {
                        keyword_counts[keyword] = 1;
                    });
                    emit(doc.gcc, keyword_counts);
                }
            }'''

reduceFunc = '''function(keys, values) {
                var result = {};
                values.forEach(function(value) {
                    for (var keyword in value) {
                        if (!result[keyword]) {
                            result[keyword] = 0;
                        }
                        result[keyword] += value[keyword];
                    }
                });
                return result;
            }'''

# Replace the URL, username, and password with your own CouchDB 
credentials
couch = couchdb.Server("http://group6:123456@172.26.131.122:5984/")
db = couch["crime_lang_tweet"]

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
