
import nltk
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.stem import PorterStemmer
import pymongo
client = pymongo.MongoClient("mongodb+srv://td_user:yYZrXfW5mS6mKcLt@gettingstarted.lwe99.mongodb.net/<dbname>?retryWrites=true&w=majority")
articles = client.scrap.articles
word_count_similar = client.scrap.word_count_similar
word_count_exact = client.scrap.word_count_exact


for item in articles.find():
    text = item['main_text']
    #define stopwords like 'a', 'the'....
    default_stopwords = set(nltk.corpus.stopwords.words('english'))
    #create list of words from text and add it to mongoDB
    words = word_tokenize(text.lower())
    articles.update_one({'_id':item['_id']}, {"$set": {'words':words}}, upsert=True)
    #clean word list from short/stopwords and add it to mongoDB
    cleaned_words = [word.replace('.','') for word in words if word not in default_stopwords and len(word) > 1]
    articles.update_one({'_id':item['_id']}, {"$set": {'cleaned_words':cleaned_words}}, upsert=True)
    # create list of sentences from text and add it to mongoDB
    sentences = sent_tokenize(text)
    articles.update_one({'_id': item['_id']}, {"$set": {'sentences': sentences}}, upsert=True)



    ps =PorterStemmer()
    RootToWord_dct = {}
    WordToRoot_dct = {}
    exact_word_count_dict = {}
    rootWord_list = []

    #calculate frequency of word in text
    fd = nltk.FreqDist(cleaned_words)


    for w in set(cleaned_words):
        #find root word. words: "likes", "liked", "likely", "liking", root word: like
        rootWord=ps.stem(w)
        rootWord_list.append(rootWord)

        #word:rootword dictionary
        WordToRoot_dct[w] = rootWord

        #this step "exact_word_count_dict[w] = fd[w]" is needless, but i don't have ttime to change it now
        exact_word_count_dict[w] = fd[w]
        #create list of words for each root word
        if rootWord not in RootToWord_dct.keys():
            RootToWord_dct[rootWord] = set()
            RootToWord_dct[rootWord].add(w)
        else:
            RootToWord_dct[rootWord].add(w)

        #print(rootWord,w)

    #caclualte sum of frequency of words with the same root and asign it to each word
    similar_word_count_dict = {}
    for w in exact_word_count_dict.keys():
        similar_word_count_dict[w] = sum([exact_word_count_dict[item] for item in RootToWord_dct[WordToRoot_dct[w]]])
    #add root word word list to expand searching capacity
    for rootword in RootToWord_dct:
        if rootword not in similar_word_count_dict:
            similar_word_count_dict[rootword] = similar_word_count_dict[list(RootToWord_dct[rootword])[0]]


    #include article ID to words and frequencies and save it to collection. this will be used for quick search. if we want to find article where words with same root (for example 'child') has the biggest frequency, it will go through this collection
    similar_word_count_dict['article_id'] = item['_id']
    word_count_similar.insert_one(similar_word_count_dict)

    # include article ID to words and frequencies and save it to collection. this will be used for quick search. if we want to find article where specific word has the biggest frequency, it will go through this collection
    exact_word_count_dict['article_id'] = item['_id']
    word_count_exact.insert_one(exact_word_count_dict)
    #marks that this document is already processed
    articles.update_one({'_id': item['_id']}, {"$set": {'processed': True}}, upsert=True)
    #todo i didn't have time to implement multiprocessing (using multiprocessing module).
    #todo set indexes on mongoDB





