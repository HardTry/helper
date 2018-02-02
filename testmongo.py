from pymongo import MongoClient

client = MongoClient("10.10.10.13:29875")
db = client.len
cursor = db.booktext.find() #{"lesson": 37})

for doc in cursor:
    # print doc
    print "Lesson ", int(doc["lesson"])
    print doc["title"]
    for line in doc["text"]:
        print line,
    print "\n"

