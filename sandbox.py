import pymongo, re

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["comparison-shopping-engine"]
product_collection = db["products"]
kota_collection = db["kota"]

for item in product_collection.find():
    
    # exp_kab = re.compile("KABUPATEN")
    location = str(item["seller_location"]).upper().replace("KAB.", "KABUPATEN")

    # if not re.search(exp_kab, location):
    #     location = "KOTA " + location
    
    kota = kota_collection.find_one({"namaKota" : {"$regex" : ".*{}.*".format(location)}})
    if kota is not None:
        idkota = kota["idKota"]
    else:
        idkota = ""

    print("{} : {}".format(idkota, location))
