import pymongo, re, nltk, string, json
from collections import defaultdict
from tqdm import tqdm
import time
# default punctuation !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

# nltk.download('punkt')

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["comparison-shopping-engine"]
product_collection = db["products"]
kota_collection = db["kota"]
index_collection = db["inverted_index_2"]
kategori_collection = db["kategori"]

def replace_kota_to_defined_kota():
    for item in product_collection.find():
        
        # exp_kab = re.compile("KABUPATEN")
        # location = str(item["seller_location"]).upper().replace("DKI JAKARTA", "JAKARTA PUSAT")
        location = str(item["seller_location"]).upper().replace("KAB.", "KABUPATEN")
        # location = str(location).upper().replace("DKI JAKARTA", "JAKARTA PUSAT")

        # if not re.search(exp_kab, location):
        #     location = "KOTA " + location
        
        kota = kota_collection.find_one({"namaKota" : {"$regex" : ".*{}.*".format(location)}})
        if kota is not None:
            idkota = kota["idKota"]
        else:
            idkota = ""

        print("{} : {}".format(idkota, location))

def title_indexing():
    products = product_collection.find({})
    for item in tqdm(products, total=products.count()) :
        # time.sleep(0.25)
        # print(item['title'])

        # kalimat.translate(str.maketrans('','',string.punctuation))

        title = str(item['title'])
        # title = 'Jual Nokia N50 - Nokia Jadul 256MB 1GB'
        title_lowered = title.lower()
        title_lowered = title_lowered.translate(str.maketrans('','','''!"#$%&'()*+,-/:;<=>?@[\]^_`{|}~'''))
        title_tokenized = nltk.word_tokenize(title_lowered)
        # print(title_tokenized)
        
        # data = defaultdict(list)
        for i in range(len(title_tokenized)):
            
            # indexes = {
            #     'doc_id' : 1,
            #     'position' : i
            # }    
            # data[title_tokenized[i]].append(indexes)

        # for d in data.items():
        #     print(d)
        
            # data = {
            #     'word' : word
            # }
            # index_collection.insert_one(data)
        
        # for item in index_collection.find():
        #     print(item)

            existed_index = index_collection.find_one({'word' : title_tokenized[i]})
            if existed_index is None: 
                data = {
                    'word' : title_tokenized[i],
                    'index' : [{
                        'doc_id' : item['_id'],
                        'position' : i
                    }]
                }
                index_collection.insert_one(data)

            else:
                new_index = {
                    'doc_id' : item['_id'],
                    'position' : i
                }
                index_collection.update_one(
                    {'_id' : existed_index['_id']},
                    {
                        '$push' : {
                            'index' : new_index
                        }
                    }
                )
            
    
def print_category():
    kategori_list = list()
    # kategori_dictionary = defaultdict(list)
    for parent in kategori_collection.find({
        "parentkategori" : ""
    }):
        appender_dictionary = dict()
        appender_dictionary[parent['idkategori']] = parent['namakategori']
        appender_dictionary['child'] = list()
        for child in kategori_collection.find({
            "parentkategori" : parent['idkategori']
        }):
            child_appender_dictionary = dict()
            child_appender_dictionary[child['idkategori']] = child['namakategori']
            appender_dictionary['child'].append(child_appender_dictionary)
        kategori_list.append(appender_dictionary)
    
    print(kategori_list)  
            

if __name__ == '__main__':

    # print('hello world')
    # replace_kota_to_defined_kota()
    # title_indexing()
    # print(string.punctuation)
    print_category()
    






