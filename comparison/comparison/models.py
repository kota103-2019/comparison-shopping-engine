import re, nltk, string, time, itertools
from bson.objectid import ObjectId
from comparison import app
from .extensions import mongo
from statistics import median, mean


class Skor :
    def __init__(self):
        self.doc_id = ObjectId()
        self.nilaiSkor = int(1)

class Produk:
    def __init__(self):
        self.idProduk = ObjectId()
        self.namaLengkapProduk = ""

    def lihatDetailProduk(self, idProduk):
        temp = mongo.db.products.find_one({"_id": ObjectId(idProduk)})
        if temp is not None:
            self.namaLengkapProduk = str(temp['title'])
            self.idKategori = str(temp['category'])
            self.idKota = str(temp['seller_location'])
            self.namaToko = str(temp['seller'])
            self.fotoProduk = str(temp['image_url'])
            self.ratingProduk = float(temp['rating'])
            self.hargaAwalProduk = float(temp['price_original'])
            self.hargaAkhirProduk = float(temp['price_final'])
            self.diskon = str(temp['discount'])
            self.kondisiBarang = int(temp['condition'])
            self.deskripsi = str(temp['description'])
            self.idOnlineMarketplace = str(temp['online_marketplace'])
            self.tautan = str(temp['url'])
            self.updateTerakhir = temp['time_taken']
        del temp


class Kota:
    def __init__(self):
        self.namaKota = ""

        
class Kategori:
    def __init__(self):
        self.kategoriDict = dict()
        self.kategoriList = list()

    def getKategori(self):
        for parent in mongo.db.kategori.find({
            "parentkategori" : ""
        }):
            appender_dictionary = dict()
            appender_dictionary['id'] = parent['idkategori']
            appender_dictionary['kategori'] = parent['namakategori']
            appender_dictionary['child'] = list()
            for child in mongo.db.kategori.find({
                "parentkategori" : parent['idkategori']
            }):
                child_appender_dictionary = dict()
                child_appender_dictionary['id'] = child['idkategori']
                child_appender_dictionary['kategori'] = child['namakategori']
                appender_dictionary['child'].append(child_appender_dictionary)
            self.kategoriList.append(appender_dictionary)
        
        return self.kategoriList
    
    def getKategoriDetail(self, id):
        return mongo.db.kategori.find_one({'idkategori' : id})

class MainPencarian:
    #Initialization
    def __init__(self):
        self.kataKunci = ""
        self.idKategori = ""
        self.filterKota = ""
        self.listIdProduk = []
        self.hargaMin = 0
        self.hargaMax = 0
        self.listKota = []
        self.jenisSort = ""
        self.caraSort = ""
        # self.infoHarga = InformasiHarga()
        # for i in mongo.db.kota.find():
        #     pKota = Kota()
        #     pKota.idKota = i['idKota']
        #     pKota.idProvinsi = i['idProvinsi']
        #     pKota.namaKota = i['namaKota']
        #     self.listKota.append(pKota)
        #     del pKota

    # def mencariProdukByKataKunci(self, page_num = 0):
    #     key = self.kataKunci        
    #     reString = ".*%s.*" % key # string untuk menampung query like untuk penggunaan regex
    #     rgx = re.compile(reString, re.IGNORECASE) # mengcompile regex dengan menginore penggunaan Upper & Lower case
    #     # filterQuery = {"title": rgx,"rating":{ "$exists": True }, "price_original":{ "$exists": True },"discount":{ "$exists": True } }
    #     filterQuery = {"title": rgx}
    #     if self.hargaMin > 0 and self.hargaMax > 0:
    #         filterQuery = {"title": rgx, "price_final":{"$gte":self.hargaMin,"$lte":self.hargaMax}, "rating":{ "$exists": True }, "price_original":{ "$exists": True },"discount":{ "$exists": True }}
    #     page_size = 30
    #     skips = page_size * (int(page_num) - 1)
    #     jml_produk = mongo.db.products.count_documents(filterQuery)
    #     dataProduk = mongo.db.products.find(filterQuery).skip(skips).limit(page_size)
    #     listOfProduk = []
    #     for i in dataProduk:
    #         ptemp = Produk()
    #         ptemp.idProduk = ObjectId(i['_id'])
    #         ptemp.namaLengkapProduk = str(i['title'])
    #         ptemp.idKategori = str(i['category'])
    #         ptemp.idKota = i['seller_location']
    #         ptemp.namaToko = str(i['seller'])
    #         ptemp.fotoProduk = str(i['image_url'])
    #         ptemp.ratingProduk = i['rating']
    #         ptemp.kondisiBarang = int(i['condition'])
    #         ptemp.hargaAwalProduk = i['price_original']
    #         ptemp.hargaAkhirProduk = i['price_final']
    #         ptemp.idOnlineMarketplace = str(i['online_marketplace'])
    #         ptemp.diskon = i['discount']
    #         ptemp.deskripsi = str(i['description'])
    #         ptemp.tautan = str(i['url'])
    #         listOfProduk.append(ptemp)
    #         del ptemp

    #     if len(listOfProduk) < 1 :
    #         return "", 0
    #     else:
    #         return listOfProduk, jml_produk

    def mencariProdukByKategori(self, isParent, page_num):
        listKategori = []
        if isParent != "true":
            idkat = self.idKategori
            listKategori.append(idkat)
        else:
            for item in mongo.db.kategori.find({"parentkategori" : self.idKategori}):
                listKategori.append(item['idkategori'])
        
        filterQuery = {"category": {"$in" : listKategori}}
        if self.hargaMin > 0 and self.hargaMax > 0:
            # filterQuery = {"category": {"$in" : listKategori} , "price_final":{"$gte":self.hargaMin,"$lte":self.hargaMax}, "rating":{ "$exists": True }, "price_original":{ "$exists": True },"discount":{ "$exists": True }}
            filterQuery = {"category": {"$in" : listKategori} , "price_final":{"$gte":self.hargaMin,"$lte":self.hargaMax}}

            if self.filterKota is not None:
                filterQuery = {"category": {"$in" : listKategori} , "price_final":{"$gte":self.hargaMin,"$lte":self.hargaMax}, "seller_location":self.filterKota}
            # filterQuery['price_final']['$gte'] = self.hargaMin
            # filterQuery['price_final']['$lte'] = self.hargaMax
        page_size = 30
        skips = page_size * (int(page_num) - 1)
        jml_produk = mongo.db.products.count_documents(filterQuery)
        print(self.jenisSort, self.caraSort, sep="/")
        if self.jenisSort:
            data = mongo.db.products.find(filterQuery).sort(str(self.jenisSort), int(self.caraSort))
        else:
            data = mongo.db.products.find(filterQuery)
        # self.infoHarga.listOfProduk = data
        # self.infoHarga.setInfoHarga()
        # dataProduk = mongo.db.products.find(filterQuery).skip(skips).limit(page_size)
        # dataProduk = data.skip(skips).limit(page_size)
        for i in mongo.db.products.aggregate([
            {
                "$match" : filterQuery
            },
            {
                "$group" : {'_id' : '$seller_location'}
            }
        ]):
            pKota = Kota()
            pKota.namaKota = i['_id']
            self.listKota.append(pKota)
            del pKota
        
        dataProduk = data

        listOfProduk = []
        for i in dataProduk:
            ptemp = Produk()
            ptemp.idProduk = ObjectId(i['_id'])
            ptemp.namaLengkapProduk = str(i['title'])
            ptemp.idKategori = str(i['category'])
            ptemp.idKota = i['seller_location']
            ptemp.namaToko = str(i['seller'])
            ptemp.fotoProduk = str(i['image_url'])
            ptemp.ratingProduk = i['rating']
            ptemp.kondisiBarang = int(i['condition'])
            ptemp.hargaAwalProduk = i['price_original']
            ptemp.hargaAkhirProduk = i['price_final']
            ptemp.idOnlineMarketplace = str(i['online_marketplace'])
            ptemp.diskon = i['discount']
            ptemp.deskripsi = str(i['description'])
            ptemp.tautan = str(i['url'])
            listOfProduk.append(ptemp)
            del ptemp

        if len(listOfProduk) < 1 :
            return "", jml_produk
        else:
            return listOfProduk, jml_produk


    def preprocessingText(self, key):
        key = key.lower()
        key = key.translate(str.maketrans('','','''!"#$%&'()*+,-/:;<=>?@[\]^_`{|}~'''))
        key = str(key).split()
        return key

    # fungsi untuk mengambil list dari document id yang mengandung 1 kata 'word' pada judul produknya
    def one_word_query(self, key):
        index = mongo.db.inverted_index.find_one({"word":key},{'_id':1 ,'word':1,'index':1})
        listWordIndx = []
        if index:
            for i in index["index"]:
                listWordIndx.append(i['doc_id'])
        return listWordIndx
    # fungsi untuk mengambil list dari documen id yang mengandung 1 frase yang sudah di preprocessing secara lengkap dan berurutan pada judul produknya
    def phrase_query(self, key_tokenized,listDocId):
        result = []
        for doc_id in listDocId:
            temp = []
            x = mongo.db.products.find_one({'_id':ObjectId(doc_id)})
            print(x['title'])
            for word in key_tokenized:
                #ambil posisi
                index = mongo.db.inverted_index.find_one({"word":word},{'index':1})
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
            skr = 0

            #while i < len(temp)-1:
            for i in range(len(temp) - 1):
                for j in range(len(temp[i])):
                    #print("tempi "+str(temp[i]))
                    #print(i)
                    for k in range(len(temp[i+1])):
                        if temp[i][j] == temp[i+1][k]:
                            #print(temp[i][j]+" "+temp[i+1][j])
                            skr+=1
                #i+=1
            rslt = Skor()
            rslt.doc_id = doc_id
            rslt.skor = skr
            result.append(rslt)
            # if set(temp[0]).intersection(*temp) :
            #     result.append(doc_id)
            #     print("frase sesuai dengan title")
            
        return result

    def mencariProdukByKataKunciRanked(self, page_num = 0):
        listWord = self.preprocessingText(self.kataKunci)
        listOfList = [] #untuk menampung list seluruh list doc_id hasil pencarian kata
        for word in listWord:
            # print("\n"+word)
            # listOfList menampung 
            listOfList.append(self.one_word_query(word))
        # Irisan dari semua List Index, untuk keperluan hanya mengambil document id yang mengandung seluruh kata pencarian
        intersectList = set(listOfList[0]).intersection(*listOfList)

        del listOfList

        listSkor =[] # untuk menampung list list dari skor skor yang berisi doc_id dan skor untuk doc_id tsb
        for i in intersectList: # hanya menggunakan doc_id yang mengandung seluruh kata pencarian
            tempSkor = Skor()
            tempSkor.doc_id = i
            listSkor.append(tempSkor)

        if len(listWord) > 1:
            # phrase query
            for i in self.phrase_query(listWord,intersectList): # query untuk mengambil doc_id yang memuat 1 frase lengkap berurutan
        
                for j in listSkor:
                    # print(j.doc_id)
                    # print(i.doc_id)
                    if j.doc_id == i.doc_id:
                        # print("skor sebelum :"+str(j.nilaiSkor))
                        j.nilaiSkor += i.skor # untuk setiap doc_id yang memuat frase lengkap tambahkan skor 1
                        # print("tambahan skor untuk :"+str(i.doc_id))
                        # print("tambah skor menjadi :"+str(j.nilaiSkor))
                        break
        #sort skor berdasarkan nilaiSkor secara descending, untuk keperluan ranking
        listSkor.sort(key=lambda x: x.nilaiSkor, reverse = True)
        listIdProduk = [ObjectId(item.doc_id) for item in listSkor]
        filterQuery = dict()
        filterQuery = {"_id": {"$in" : listIdProduk}}
        # filterQuery['_id']['$in'] = listIdProduk
        if self.hargaMin > 0 and self.hargaMax > 0:
            # filterQuery = {"_id": {"$in" : listIdProduk} , "price_final":{"$gte":self.hargaMin,"$lte":self.hargaMax}, "rating":{ "$exists": True }, "price_original":{ "$exists": True },"discount":{ "$exists": True }}
            filterQuery = {"_id": {"$in" : listIdProduk} , "price_final":{"$gte":self.hargaMin,"$lte":self.hargaMax}}

            if self.filterKota != "":
                filterQuery = {"_id": {"$in" : listIdProduk} , "price_final":{"$gte":self.hargaMin,"$lte":self.hargaMax}, "seller_location":self.filterKota}
            # filterQuery['price_final']['$gte'] = self.hargaMin
            # filterQuery['price_final']['$lte'] = self.hargaMax
        listOfProduk = [] 
        page_size = 30
        skips = page_size * (int(page_num) - 1)
        jml_produk = mongo.db.products.count_documents(filterQuery)
        if self.jenisSort:
            data = mongo.db.products.find(filterQuery).sort(str(self.jenisSort), int(self.caraSort))
        else:
            data = mongo.db.products.find(filterQuery)
        # dataProduk = mongo.db.products.find(filterQuery).skip(skips).limit(page_size)
        # dataProduk = data.skip(skips).limit(page_size)
        dataProduk = data

        for i in mongo.db.products.aggregate([
            {
                "$match" : filterQuery
            },
            {
                "$group" : {'_id' : '$seller_location'}
            }
        ]):
            pKota = Kota()
            pKota.namaKota = i['_id']
            self.listKota.append(pKota)
            del pKota

        for i in dataProduk:
            ptemp = Produk()
            ptemp.idProduk = ObjectId(i['_id'])
            ptemp.namaLengkapProduk = str(i['title'])
            ptemp.idKategori = str(i['category'])
            ptemp.idKota = i['seller_location']
            ptemp.namaToko = str(i['seller'])
            ptemp.fotoProduk = str(i['image_url'])
            ptemp.ratingProduk = i['rating']
            ptemp.kondisiBarang = int(i['condition'])
            ptemp.hargaAwalProduk = i['price_original']
            ptemp.hargaAkhirProduk = i['price_final']
            ptemp.idOnlineMarketplace = str(i['online_marketplace'])
            ptemp.diskon = i['discount']
            ptemp.deskripsi = str(i['description'])
            ptemp.tautan = str(i['url'])
            listOfProduk.append(ptemp)
            del ptemp

        if len(listOfProduk) < 1 :
            return "", jml_produk
        else:
            return listOfProduk, jml_produk

    def compare(self, listIdProduk):
        listIdProduk = [ObjectId(item) for item in listIdProduk]
        filterQuery = {"_id": {"$in" : listIdProduk}}
        dataProduk = mongo.db.products.find(filterQuery)
        listOfProduk = []
        for i in dataProduk:
            ptemp = Produk()
            ptemp.idProduk = ObjectId(i['_id'])
            ptemp.namaLengkapProduk = str(i['title'])
            ptemp.idKategori = str(i['category'])
            ptemp.idKota = i['seller_location']
            ptemp.namaToko = str(i['seller'])
            ptemp.fotoProduk = str(i['image_url'])
            ptemp.ratingProduk = i['rating']
            ptemp.kondisiBarang = int(i['condition'])
            ptemp.hargaAwalProduk = i['price_original']
            ptemp.hargaAkhirProduk = i['price_final']
            ptemp.idOnlineMarketplace = str(i['online_marketplace'])
            ptemp.diskon = i['discount']
            ptemp.deskripsi = str(i['description'])
            ptemp.tautan = str(i['url'])
            ptemp.updateTerakhir = i['time_taken']
            listOfProduk.append(ptemp)
            del ptemp

        if len(listOfProduk) < 1 :
            return ""
        else:
            return listOfProduk


class InformasiHarga:
    def __init__(self):
        self.listOfProduk = []
        self.hargaMin = 0.0
        self.hargaMax = 0.0
        self.hargaMean = 0.0
        self.hargaMed = 0.0
    
    def setInfoHarga(self):
        if(len(self.listOfProduk)>0):
            listHarga = []
        
            for i in self.listOfProduk:
                listHarga.append(i.hargaAkhirProduk)
        
            self.hargaMax = max(listHarga)
            self.hargaMin = min(listHarga)
            self.hargaMean = mean(listHarga)
            self.hargaMed = median(listHarga)
