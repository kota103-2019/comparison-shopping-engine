import pymongo


client = pymongo.MongoClient("mongodb+srv://KoTA-103:bismillah@cluster0-sr9cz.mongodb.net/test?retryWrites=true&w=majority")
db = client.test

print(db)