import scrapy, nltk
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from webcrawler.spiders.bukalapak import BukalapakSpider
from webcrawler.spiders.tokopedia import TokopediaSpider
from webcrawler.spiders.lazada import LazadaSpider
from webcrawler.spiders.jd_id import JdIdSpider

from connection import colInvIndx, colProducts

stopword = ['promo','jual','ready','laris','dijual','stock','terlaris','terbaik','stok','murah',
            'kualitas','termurah','kwalitas'
            ]

def filterStopword(listWord:list ,stopword:list):
    cleaned = [ token for token in listWord \
                if not token in stopword]
    return cleaned

def title_indexing():
    for item in colProducts.find({}):
        # print(item['title'])

        # kalimat.translate(str.maketrans('','',string.punctuation))

        title = str(item['title'])
        # title = 'Jual Nokia N50 - Nokia Jadul 256MB 1GB'
        title_lowered = title.lower()
        title_lowered = title_lowered.translate(str.maketrans('','','''!"#$%&'()*+,-/:;<=>?@[\]^_`{|}~'''))
        #title_tokenized = nltk.word_tokenize(title_lowered)
        title_tokenized = str(title_lowered).split()
        title_tokenized = filterStopword(title_tokenized,stopword)
        # print(title_tokenized)
        
        # data = defaultdict(list)
        for i in range(len(title_tokenized)):
            
            # indexes = {
            #     'doc_id' : 1,
            #     'position' : i
            # }    
            # data[title_tokenized[i]].append(indexes)

        # for d in data.items():
        #     print(d)
        
            # data = {
            #     'word' : word
            # }
            # index_collection.insert_one(data)
        
        # for item in index_collection.find():
        #     print(item)

            existed_index = colInvIndx.find_one({'word' : title_tokenized[i]})
            if existed_index is None: 
                data = {
                    'word' : title_tokenized[i],
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

def prosesCrawl():
    process = CrawlerProcess(get_project_settings())
    #process.crawl(BukalapakSpider)
    process.crawl(TokopediaSpider)
    #process.crawl(JdIdSpider)
    process.start()
    print("\n\nPembuatan Index Product kembali")
    colProducts.reindex()
    print("\n\nPembuatan Inverted Index")
    colInvIndx.drop()
    title_indexing()