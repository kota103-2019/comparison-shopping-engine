from bson.objectid import ObjectId
import re
from comparison import app
from .extensions import mongo

class Produk:
    def __init__(self):
        self.namaLengkapProduk = ""

class Kota:
    def __init__(self):
        self.namaKota = ""
        
class MainPencarian:
    #Initialization
    def __init__(self):
        self.kataKunci = ""
        self.listIdProduk = []
        self.hargaMin = 0
        self.hargaMax = None

    def mencariProdukByKataKunci(self):
        key = self.kataKunci        
        reString = ".*%s.*" % key # string untuk menampung query like untuk penggunaan regex
        rgx = re.compile(reString, re.IGNORECASE) # mengcompile regex dengan menginore penggunaan Upper & Lower case
        
        #data = mongo.db.produk.find({"price_final":{"$gte":self.hargaMin}},{"title": rgx })
        listKota = []
        for i in mongo.db.kota.find():
            pKota = Kota()
            pKota.idKota = i['idKota']
            pKota.idProvinsi = i['idProvinsi']
            pKota.namaKota = i['namaKota']
            listKota.append(pKota)
            del pKota
            
        dataProduk = mongo.db.produk.find({"title": rgx,"rating":{ "$exists": True }, "price_original":{ "$exists": True },"discount":{ "$exists": True } })
        listOfProduk = []
        for i in dataProduk:
            ptemp = Produk()
            ptemp.idProduk = ObjectId(i['_id'])
            ptemp.namaLengkapProduk = str(i['title'])
            ptemp.idKategori = str(i['category'])
            ptemp.idKota = str(i['seller_location'])
            ptemp.namaToko = str(i['seller'])
            ptemp.fotoProduk = str(i['image_url'])
            ptemp.ratingProduk = i['rating']
            #ptemp.jumlahRating = int(i[''])
            ptemp.hargaAwalProduk = i['price_original']
            ptemp.diskon = float(i['discount'])
            #ptemp.terjual = 0
            ptemp.kondisiBarang = int(i['condition'])
            ptemp.deskripsi = str(i['description'])
            ptemp.idOnlineMarketplace = str(i['online_marketplace'])
            ptemp.tautan = str(i['url'])

            listOfProduk.append(ptemp)
            del ptemp
        
        if len(listOfProduk) < 1 :
            return ""
        else:
            return listOfProduk



class InformasiHarga:
    def __init__(self):
        self.listIdProduk = []
        self.hargaMin = 0.0
        self.hargaMax = 0.0
        self.hargaMean = 0.0
        self.hargaMed = 0.0
    
    def cariHargaMin(listIdProduk):
        return 0
    
    def cariHargaMax(listIdProduk):
        return True
    def hitungHargaMean(listIdProduk):
        return True
    def hitungHargaMed(listIdProduk):
        return True
#class