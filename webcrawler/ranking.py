import pymongo, re, nltk, string, time
from bson.objectid import ObjectId

try:
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    client.server_info()
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(err)
db = client["comparison-shopping-engine"]
colInv = db["invertedIndex"]

stopword = ['promo','jual','ready','laris','dijual','stock','terlaris','terbaik','stok','murah',
            'kualitas','termurah','kwalitas','dan','atau'
            ]

def filterStopword(listWord:list ,stopword:list):
    cleaned = [ token for token in listWord \
                if not token in stopword]
    return cleaned

class skor :
    def __init__(self):
        self.doc_id = ObjectId()
        self.nilaiSkor = int(1)

# fungsi untuk mengambil list dari document id yang mengandung 1 kata 'word' pada judul produknya
def one_word_query(key):
    index = colInv.find_one({"word":key},{'_id':1 ,'word':1,'index':1})
    listWordIndx = []
    if index:
        for i in index["index"]:
            listWordIndx.append(i['doc_id'])
    return listWordIndx
# fungsi untuk mengambil list dari documen id yang mengandung 1 frase yang sudah di preprocessing secara lengkap dan berurutan pada judul produknya
def phrase_query(key_tokenized,listDocId):
    result = []
    for doc_id in listDocId:
        temp = []
        colProduct = db["products"]
        x = colProduct.find_one({'_id':ObjectId(doc_id)})
        print(x['title'])
        for word in key_tokenized:
            #ambil posisi
            index = colInv.find_one({"word":word},{'index':1})
            temp2 = []
            for i in index['index']:
                if i['doc_id'] == doc_id:
                    temp2.append(i['position'])
            #tambahkan ke list
            temp.append(temp2)
        print(temp)
        for i in range(len(temp)):
            for ind in range(len(temp[i])):
                temp[i][ind] -= i
        if set(temp[0]).intersection(*temp) :
            result.append(doc_id)
            #print("frase sesuai dengan title")
    return result

print("Pencarian Test\n")
key = str(input("Input kata kunci pencarian:"))
start = time.process_time()
key = key.lower()
key = key.translate(str.maketrans('','','''!"#$%&'()*+,-/:;<=>?@[\]^_`{|}~'''))
key_tokenized = str(key).split()
#key_tokenized = filterStopword(key_tokenized,stopword)
#key_tokenized = nltk.word_tokenize(key)
#for i in range(len(key_tokenized)):
#    print("\n"+key_tokenized[i])

listOfList = [] #untuk menampung list seluruh list doc_id hasil pencarian kata
for word in key_tokenized:
    print("\n"+word)
    # listOfList menampung 
    listOfList.append(one_word_query(word))
# Irisan dari semua List Index, untuk keperluan hanya mengambil document id yang mengandung seluruh kata pencarian
intersectList = set(listOfList[0]).intersection(*listOfList)

del listOfList

listSkor =[] # untuk menampung list list dari skor skor yang berisi doc_id dan skor untuk doc_id tsb
for i in intersectList: # hanya menggunakan doc_id yang mengandung seluruh kata pencarian
    tempSkor = skor()
    tempSkor.doc_id = i
    listSkor.append(tempSkor)

if len(key_tokenized) > 1:
    # phrase query
    for i in phrase_query(key_tokenized,intersectList): # query untuk mengambil doc_id yang memuat 1 frase lengkap berurutan
   
        for j in listSkor:
            #print(j.doc_id)
            #print(i)
            if j.doc_id == i:
                # print("skor sebelum :"+str(j.nilaiSkor))
                j.nilaiSkor += 1 # untuk setiap doc_id yang memuat frase lengkap tambahkan skor 1
                print("tambahan skor untuk :"+str(i))
                print("tambah skor menjadi :"+str(j.nilaiSkor))
                break
#sort skor berdasarkan nilaiSkor secara descending, untuk keperluan ranking
listSkor.sort(key=lambda x: x.nilaiSkor, reverse = True) 
colProduct = db["products"]
for i in listSkor:
    temp = colProduct.find_one({'_id':ObjectId(i.doc_id)})
    print(i.doc_id)
    print(temp['title'])
    print(i.nilaiSkor)

print(time.process_time() - start)