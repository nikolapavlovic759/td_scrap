# td_scrap
spider is run by command "scrapy crawl quotes" from top level directory. I run it through Anaconda prompt. It will populate MongoDB with aricles data. 
mongo connection string is mongodb+srv://td_user:yYZrXfW5mS6mKcLt@gettingstarted.lwe99.mongodb.net/<dbname>?retryWrites=true&w=majority
next to run is script data_processing.py, which generate some additional data. i run it directly from PyCharm
articles are searched with find_articles.py. searching parameters are through python input function (i also run it through PyCharm). it searched articles for provided keywords, and returns them decendingly by frequency of serached words. There are two modes, first one look for exact match of the word, and second one look for similar words as well (words with the same root word). 
  
Code sholud be optimized (some loops could be avoided) and multiprocessing can be implemented, but i din't have enough time. 
