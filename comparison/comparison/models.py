
class KataKunci:
    def __init__(self, katakunci):
        self.katakunci = katakunci

class OnlineMarketplace:
    def __init__(self, idOnlineMarketplace, namaMarketplace, alamatWebsite):
        self.idOnlineMarketplace = idOnlineMarketplace
        self.namaMarketplace = namaMarketplace
        self.alamatWebsite = alamatWebsite

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