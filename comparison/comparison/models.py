from bson.objectid import ObjectId
import re
from comparison import app
from .extensions import mongo

class Produk:
    def __init__(self):
        self.idProduk = ObjectId()
        self.namaLengkapProduk = ""

    def lihatDetailProduk(self, idProduk):
        temp = mongo.db.produk.find_one({"_id": ObjectId(idProduk)})
        if temp is not None:
            self.namaLengkapProduk = str(temp['title'])
            self.idKategori = str(temp['category'])
            self.idKota = str(temp['seller_location'])
            self.namaToko = str(temp['seller'])
            self.fotoProduk = str(temp['image_url'])
            self.ratingProduk = float(temp['rating'])
            #ptemp.jumlahRating = int(i[''])
            self.hargaAwalProduk = float(temp['price_original'])
            self.hargaAkhirProduk = float(temp['price_final'])
            self.diskon = float(temp['discount'])
            #ptemp.terjual = 0
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
        self.namaKategori = ""

class MainPencarian:
    #Initialization
    def __init__(self):
        self.kataKunci = ""
        self.listIdProduk = []
        self.hargaMin = 0
        self.hargaMax = None
        self.listKota = []
        for i in mongo.db.kota.find():
            pKota = Kota()
            pKota.idKota = i['idKota']
            pKota.idProvinsi = i['idProvinsi']
            pKota.namaKota = i['namaKota']
            self.listKota.append(pKota)
            del pKota

    def mencariProdukByKataKunci(self):
        key = self.kataKunci        
        reString = ".*%s.*" % key # string untuk menampung query like untuk penggunaan regex
        rgx = re.compile(reString, re.IGNORECASE) # mengcompile regex dengan menginore penggunaan Upper & Lower case
        filterQuery = {"title": rgx,"rating":{ "$exists": True }, "price_original":{ "$exists": True },"discount":{ "$exists": True } }
        if self.hargaMin > 0 and self.hargaMax > 0:
            filterQuery = {"title": rgx, "price_final":{"$gte":self.hargaMin,"$lte":self.hargaMax}, "rating":{ "$exists": True }, "price_original":{ "$exists": True },"discount":{ "$exists": True }}
        dataProduk = mongo.db.produk.find(filterQuery)
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
            ptemp.hargaAkhirProduk = i['price_final']
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
    
    def cariHargaMin(self, listOfProduk):
        min = listOfProduk[0].hargaAkhirProduk
        for i in listOfProduk:
            if i.hargaAkhirProduk < min:
                min = i.hargaAkhirProduk
        return min
    
    def cariHargaMax(self, listOfProduk):
        max = listOfProduk[0].hargaAkhirProduk
        for i in listOfProduk:
            if i.hargaAkhirProduk > max:
                max = i.hargaAkhirProduk
        return max

    def hitungHargaMean(listOfProduk):
        return True
    def hitungHargaMed(listOfProduk):
        return True
    
    def setInfoHarga(self, listOfProduk):
        self.hargaMax = self.cariHargaMax(listOfProduk)
        self.hargaMin = self.cariHargaMin(listOfProduk)
#class