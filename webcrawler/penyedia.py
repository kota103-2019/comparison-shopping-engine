import crawl
import time
from kategori import kategori, addCategory
import pymongo


if __name__ == '__main__':
    end = False
    while end!=True:
        print("\t**********************************************")
        print("\t***  Aplikasi Penyedia Data  ***")
        print("\t**********************************************")
        print("\nMenu pilihan :")
        print("1. Lakukan pengambilan data")
        print("2. Tambahkan Kategori Baru")
        print("3. Keluar dari Aplikasi")
        x = input("\nMasukan pilihan :")
        if x == '1':
            #start = time.process_time()
            crawl.prosesCrawl()
            #print(time.process_time() - start)
            
            end = True
        elif x == '2':
            #add kategori
            addCategory()
        elif x == '3':
            end = True
