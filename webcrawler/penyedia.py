import crawl
import time
from kategori import *
import pymongo



end = False
while end!=True:
    print("\t**********************************************")
    print("\t***  Aplikasi Penyedia Data  ***")
    print("\t**********************************************")
    print("\nMenu pilihan :")
    print("\n1. Lakukan pengambilan data")
    print("\n2. Tambahkan Kategori Baru")
    print("\n3. Keluar dari Aplikasi")
    x = input("\nMasukan pilihan :")
    if x == '1':
        start = time.process_time()
        crawl.prosesCrawl()
        print(time.process_time() - start)
        end = True
    elif x == '2':
        #add kategori
        addCategory()
    elif x == '3':
        end = True

