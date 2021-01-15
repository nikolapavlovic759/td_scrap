import scrapy
import time
import pymongo
client = pymongo.MongoClient("mongodb+srv://td_user:yYZrXfW5mS6mKcLt@gettingstarted.lwe99.mongodb.net/<dbname>?retryWrites=true&w=majority")
articles = client.scrap.articles


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    #define main page
    def start_requests(self):
        yield scrapy.Request(url='https://www.theguardian.com/international', callback=self.prepare_hrefs)

    # define main pagesearch for articles hrefs on main page
    def prepare_hrefs(self, response):
        data = [a.attrib['href'] for a in response.xpath('//a[@data-link-name="article"]')]
        for dat in data:
            print(dat)
            yield scrapy.Request(url=dat, callback=self.parse)

    #parse articles
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{str(time.time())}.html'
        #url
        url = (response.url)
        #title
        title = response.xpath('//title/text()').get()
        #description
        description = response.xpath('//div[@class="css-1ji4n2i"]/div[@class="css-1ueujop"]/p/text()').get()
        #main_text
        main_text = response.xpath('//p[@class="css-38z03z"]/text()').getall()
        # main topics
        main_topic = response.xpath('//li[@class="css-py6pl9"]/a[@class="css-dlavgv"]/text()').get()
        #topics
        topics = response.xpath('//a[@class="css-dlavgv"]/text()').getall()


        #log articles which could not be scarpped completely. this is due to subscription request on web page. this require some additional programming
        urls_without_text = []
        if len(main_text)>0:
            #exclude articles which are not scarpped completely, otherwise insert in mongodb
            if articles.find_one({ "url": url }) is None:
                articles.insert_one({'url':url,
                                     'title': title.replace('  ',' '),
                                     'description': description,
                                     'main_text': ' '.join(main_text).replace('  ',' '),
                                     'main_topic': main_topic,
                                     'topics': topics
                                     })
        else:
            urls_without_text.append(url)
        if len(urls_without_text)>0:
            f = open("errors.txt", "a")
            f.write('\n'.join(urls_without_text))
            f.close()
