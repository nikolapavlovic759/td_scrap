import pymongo
from bson.son import SON
client = pymongo.MongoClient("mongodb+srv://td_user:yYZrXfW5mS6mKcLt@gettingstarted.lwe99.mongodb.net/<dbname>?retryWrites=true&w=majority")
articles = client.scrap.articles

#words to be searched on articles. it can search for several words - in that case it will sum up their frequency
key_words = input('Input search key words separated by comma (trump,impeachment):').split(',')
key_words = [item.lower().strip().replace('"','').replace("'","") for item in key_words if item!='']

#should it search for exact match (child!=children) or count words the same root as well (child==children)
serach_type = input('Search by exact match (child!=children) or accept word variation(child==children))? posible values: exact, variation, :')
serach_type = serach_type.lower().strip().replace('"','').replace("'","")
if serach_type not in ['exact', 'variation']:
    print("Only values 'exact' and 'variation' can be accepted. Try again. ")
if serach_type == 'exact':
    searchdat = client.scrap.word_count_exact
else:
    searchdat = client.scrap.word_count_similar

#define which elemtns to print (fileds in mongoDB document)
print_elements = input('Input article elements to print (posible options: number_of_matches, url, title, description, main_text, main_topic, topics, words, cleaned_words, sentences):').split(',')
print_elements = [item.lower().strip().replace('"','').replace("'","") for item in print_elements if item!='']
#define how many articles to print, sorted decending by frequncy of searched words
print_limit = int(input('Input number of top results to print:'))

#search for articles with highest frequency of searched words
words = [{'$ifNull': ['$' + w , 0]} for w in key_words]
pipeline = [{"$project":{
    'article_id':'$article_id',
    'freq':{ '$add' : words}}},
        {"$sort": SON([("freq", -1)])}
        ,{"$match": { 'freq' : { '$gt': 0 }}}
        ,{'$limit':print_limit}]


for x in searchdat.aggregate(pipeline):
    #print frequency of searched words
    if 'number_of_matches' in print_elements:
        print(x['freq'])
    # print selected part of articles
    for y in articles.find({'_id':x['article_id']},{ "_id": 0, 'url':1, 'title':1, 'description':1, 'main_text':1, 'main_topic':1, 'topics':1, 'words':1, 'cleaned_words':1, 'sentences':1}):
        for element in print_elements:
            if element in ['url', 'title', 'description', 'main_text', 'main_topic', 'topics', 'words', 'cleaned_words', 'sentences']:
                print(element.strip() + ': ' + str(y[element.strip()]))





