import crawl
import time
from models import kategori, mainPenyedia
import pymongo
from connection import colKategori

if __name__ == '__main__':
    end = False
    while end!=True:
        print("\t**********************************************")
        print("\t***  Aplikasi Penyedia Data  ***")
        print("\t**********************************************")
        print("\nMenu pilihan :")
        print("1. Lakukan pengambilan data")
        print("2. Tambah Sumber Data Kategori")
        print("3. Keluar dari Aplikasi")
        x = input("\nMasukan pilihan :")
        if x == '1':
            #start = time.process_time()
            crawl.prosesCrawl()
            #print(time.process_time() - start)
            
            #end = True
        elif x == '2':
            main = mainPenyedia()
            #add kategori
            print("Data Kategori")
            j = 0
            for i in main.listKategori:
                print(j+1,". ",i['namakategori'])
                j+=1
            print("99. Tambah Kategori Baru \n")
            print("Pilih kategori untuk ditambahkan datanya !")
            no = int(input(":"))
            #update
            if no != 99 :
                tempkat = main.listKategori[no-1]
                main.addCategory(False,tempkat["_id"])
            #Baru
            elif no == 99 :
                main.addCategory(True,no)
            del main
        elif x == '3':
            end = True
