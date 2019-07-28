import pymongo

try:
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    client.server_info()
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(err)
db = client["comparison"]
colKategori = db["kategori"]
colProducts = db["products"]
colInvIndx = db["invertedIndex"]