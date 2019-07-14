import pymongo

try:
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    client.server_info()
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(err)
db = client["comparison-shopping-engine"]
colKategori = db["kategori"]

#listKategori = colKategori.find()
class kategori:
    def __init__(self):
        self.namaKategori = ""
        self.bukalapak = []
        self.tokopedia = []
        self.lazada = []
        self.jdId = []
        
    def addNewTautan(self, idOnlineMarketplace):
        print("\nMasukan tautan kategori !")
        tautan = str(input("\n:"))
        #Pengecekan duplikasi tautan Kategori
        sudahAda = False
        nameOM = ''
        if idOnlineMarketplace == 1:
            nameOM = 'bukalapak'
        elif idOnlineMarketplace ==2:
            nameOM = 'tokopedia'
        elif idOnlineMarketplace ==3:
            nameOM = 'lazada'
        elif idOnlineMarketplace ==4:
            nameOM = 'jdId'
        for i in colKategori.find():
            for url in i[nameOM]:
                if url == tautan:
                    sudahAda = True
                    break
        #Jika terjadi duplikasi tautan
        if sudahAda:
                print("Tambah tautan gagal, tautan kategori sudah ada sebelumnya!")
        #Jika tidak duplikasi
        else:
            if idOnlineMarketplace == 1:
                self.bukalapak.append(tautan)
            elif idOnlineMarketplace ==2:
                self.tokopedia.append(tautan)
            elif idOnlineMarketplace ==3:
                self.lazada.append(tautan)
            elif idOnlineMarketplace ==4:
                self.jdId.append(tautan)

def addCategory():
    newKat = kategori()
    newKat.namaKategori =input ("\nMasukan Nama Kategori:")
    tambah = True
    while tambah:
        #idOnlineMarketplace = kategori.pilihOnlineMarket()
        print("\nPilih Online Marketplace untuk ditambahkan tautannya")
        print("\n1. Bukalapak")
        print("\n2. Tokopedia")
        print("\n3. Lazada")
        print("\n4. Jd-ID")
        print("\n9. Batalkan penambahan\n")
        idOnlineMarketplace = int(input(":"))
        if idOnlineMarketplace > 4 or idOnlineMarketplace< 1 :
            print("Pilihan tidak sesuai ! pilih diantara angka 1-4")
        elif idOnlineMarketplace == 9:
            del newKat
            break
        else:
            newKat.addNewTautan(idOnlineMarketplace)
        print("\n Tambah tautan lagi? (y/n)")
        x = str(input("\n"))
        x.lower()
        if x =="n":
            tambah = False
        else:
            tambah = True
    newIdKat = "id"+newKat.namaKategori
    #penambahan idKategori pada kategori sebelumnya (untuk Tree)
    j = False
    tempIdKat = "PerlKantor"
    while j == False :
        tempKat = colKategori.find_one({"idkategori":tempIdKat})
        #jika next kategori NULL
        if not tempKat['next']:
            #update next dengan idKategori baru
            colKategori.update_one({"idkategori":tempIdKat},{ "$set": { "next":newIdKat} })
            break
        #jika tidak, lihat kategori next tsb
        else:
            tempIdKat = tempKat['next']
            j = True
    colKategori.insert_one({"namakategori" : newKat.namaKategori,
    "idkategori":newIdKat,
    "parentkategori":"",
    "firstchild":"",
    "next":"",
    "bukalapak":newKat.bukalapak,
    "tokopedia":newKat.tokopedia,
    "lazada":newKat.lazada,
    "jdId":newKat.jdId})    
    del newKat