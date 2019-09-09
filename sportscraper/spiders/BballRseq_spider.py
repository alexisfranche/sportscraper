import scrapy

class BballRseqSpider(scrapy.Spider):
    name = "BballRSEQ"
    start_urls = [
        'http://www.sportetudiant-stats.com/universitaire/basketball-m/'
    ]

    #Default method that framework will seek
    def parse(self, response):


        return