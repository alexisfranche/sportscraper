import scrapy


class SportSpider(scrapy.Spider):
    name = "sport"
    start_urls = [
        'http://tornades.org/horaire-novice-masculin-a/'
    ]

    def parse(self, response):
       # for date in response.css('#content > div.entry-content > table:nth-child(1) > tbody > tr:nth-child(2) > td:nth-child(1)'):
            yield {
                'date': response.css('#content > div.entry-content > table:nth-child(1) > tbody > tr:nth-child(2) > td:nth-child(1)::text').get()

            }