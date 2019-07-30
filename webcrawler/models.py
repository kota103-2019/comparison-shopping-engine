from tqdm import tqdm
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from webcrawler.spiders.bukalapak import BukalapakSpider
from webcrawler.spiders.tokopedia import TokopediaSpider
from webcrawler.spiders.lazada import LazadaSpider
from webcrawler.spiders.jd_id import JdIdSpider

from connection import colInvIndx, colProducts,colKategori

class kategori:
    def __init__(self):
        self.namaKategori = ""
        self.bukalapak = []
        self.tokopedia = []
        self.lazada = []
        self.jdId = []
        
    def addNewTautan(self, idOnlineMarketplace,urlSumberData):
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
                if url == urlSumberData:
                    sudahAda = True
                    break
        #Jika terjadi duplikasi tautan
        if sudahAda:
                print("Tambah tautan gagal, tautan kategori sudah ada sebelumnya!")
        #Jika tidak duplikasi
        else:
            if idOnlineMarketplace == 1:
                self.bukalapak.append(urlSumberData)
            elif idOnlineMarketplace ==2:
                self.tokopedia.append(urlSumberData)
            elif idOnlineMarketplace ==3:
                self.lazada.append(urlSumberData)
            elif idOnlineMarketplace ==4:
                self.jdId.append(urlSumberData)
    def addNewCategory(self, namaKategori):
        tambah = True
        self.namaKategori = namaKategori
        while tambah:
            print("\nPilih Online Marketplace untuk ditambahkan tautannya")
            print("1. Bukalapak")
            print("2. Tokopedia")
            print("3. Lazada")
            print("4. Jd-ID")
            print("9. Batalkan penambahan\n")
            idOnlineMarketplace = int(input("pilihan:"))
            if idOnlineMarketplace == 9:
                #del newKat
                break
            elif idOnlineMarketplace > 4 or idOnlineMarketplace< 1 :
                print("Pilihan tidak sesuai ! pilih diantara angka 1-4")
            
                #break
            else:
                print("Masukan url Sumber data !")
                urlSumberData = str(input())
                #addNewTautan
                self.addNewTautan(idOnlineMarketplace,urlSumberData)
                print("\n Tambah tautan lagi? (y/n)")
                x = str(input("\n"))
                x.lower()
                if x =="n":
                    tambah = False
                    #merubah id next pada kategori terakhir dengan id kategori baru
                    j = False
                    tempIdKat = "PerlKantor"
                    while j == False :
                        tempKat = colKategori.find_one({"idkategori":tempIdKat})
                        #jika next kategori NULL
                        if not tempKat['next']:
                            #update next dengan idKategori baru
                            colKategori.update_one({"idkategori":tempIdKat},{ "$set": { "next":"id"+self.namaKategori} })
                            break
                        #jika tidak, lihat kategori next tsb
                        else:
                            tempIdKat = tempKat['next']
                            j = True
                            colKategori.insert_one({"namakategori" : self.namaKategori,
                        "idkategori":"id"+self.namaKategori,
                        "parentkategori":"",
                        "firstchild":"",
                        "next":"",
                        "bukalapak":self.bukalapak,
                        "tokopedia":self.tokopedia,
                        "lazada":self.lazada,
                        "jdId":self.jdId})
                            print("Penambahan Kategori Selesai")
                else:
                    tambah = True
        
    def updateCategory(self,idKategori):
        tambah = True
        self.idKategori = idKategori
        while tambah:
            print("\nPilih Online Marketplace untuk ditambahkan tautannya")
            print("1. Bukalapak")
            print("2. Tokopedia")
            print("3. Lazada")
            print("4. Jd-ID")
            print("\n9. Batalkan penambahan\n")
            idOnlineMarketplace = int(input(":"))
            if idOnlineMarketplace > 4 or idOnlineMarketplace< 1 :
                print("Pilihan tidak sesuai ! pilih diantara angka 1-4")
            elif idOnlineMarketplace == 9:
                #del newKat
                break
            else:
                print("Masukan url Sumber data !")
                urlSumberData = str(input())
                #addNewTautan
                self.addNewTautan(idOnlineMarketplace,urlSumberData)
            print("\n Tambah tautan lagi? (y/n)")
            x = str(input("\n"))
            x.lower()
            if x =="n":
                tambah = False
                #update
                colKategori.update_one(
                    {'_id' : idKategori},
                    {
                        '$push' : {
                            'bukalapak' : {'$each':self.bukalapak}
                            ,
                            'tokopedia' : {'$each':self.tokopedia},
                            'lazada' : {'$each':self.lazada},
                            'jdId' : {'$each':self.jdId}
                        }
                    }
                )
                print("Penambahan Kategori Selesai")
            else:
                tambah = True


class mainPenyedia:
    def __init__(self):
        self.listKategori = []
        for i in colKategori.find({},{"_id":1,"namakategori":1}):
            self.listKategori.append(i)
        self.listCrawler = []
        self.listCrawler.append(BukalapakSpider)
        self.listCrawler.append(LazadaSpider)
        self.listCrawler.append(TokopediaSpider)
        self.listCrawler.append(JdIdSpider)
    
    def preprocessingText(self,text):
        text = text.lower()
        punct = '''!#$%&()*+.,-/:;<=>?@[\]^_{|}~'''
        text = text.translate(str.maketrans(punct,' '*len(punct),'''"'`'''))
        text = str(text).split()
        return text

    def addCategory(self, newKat,pilihan):
        ktgr = kategori()
        if newKat :
            namaKategori = str(input("Masukan nama Kategori baru!\n"))
            ktgr.addNewCategory(namaKategori)
            del ktgr
        else :
            print("update category")
            #print(pilihan)
            kat = colKategori.find_one({"_id":pilihan})
            #print("update category", kat["namakategori"])
            ktgr.updateCategory(kat["_id"])
            del ktgr
    
    def title_indexing(self):
        x = colProducts.find({})
        for item in tqdm(x,total=x.count()):        
            listWord = []
            title = str(item['title'])
            temp = (self.preprocessingText(title))
            for i in temp:
                listWord.append(i)
            for i in range(len(listWord)):    
                existed_index = colInvIndx.find_one({'word' : listWord[i]})
                if existed_index is None: 
                    data = {
                        'word' : listWord[i],
                        'index' : [{
                            'doc_id' : item['_id'],
                            'position' : i
                        }]
                    }
                    colInvIndx.insert_one(data)
                else:
                    new_index = {
                        'doc_id' : item['_id'],
                        'position' : i
                    }
                    colInvIndx.update_one(
                        {'_id' : existed_index['_id']},
                        {
                            '$push' : {
                                'index' : new_index
                            }
                        }
                    )
                colInvIndx.reindex()
    def startCrawlAndIndex(self):
        process = CrawlerProcess(get_project_settings())
        for spider in self.listCrawler:
            process.crawl(spider)
        process.start()
        print("\n\nPembuatan Index Product kembali")
        colProducts.reindex()
        print("\n\nPembuatan Inverted Index, Proses ini akan memakan waktu, tunggu sampai selesai")
        colInvIndx.drop()
        self.title_indexing()
        print("Pengambilan Data dan pembuatan Index berhasil")