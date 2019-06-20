
import re
from .extensions import mongo

class MainPencarian:
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
        data = mongo.db.produk.find({"title": rgx })
        #if data.retrieved >= 0 :
        return data


#class Produk:
#    def __init__(self):

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