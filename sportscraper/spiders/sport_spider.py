import scrapy


class SportSpider(scrapy.Spider):
    name = "sport"
    start_urls = [
        'http://tornades.org/horaire-novice-masculin-a/'
    ]

    def parse(self, response):
        table = response.css("#content > div.entry-content > table:nth-child(1)")
        body = table.css("tbody")
        ctn = body.css("tr")
        for data in ctn.css("tr"):
            infoNode = data.css("td")
            print(infoNode)
            yield {
                    'Event date': str(infoNode[0].get()),
                    'Time': str(infoNode[1].get()),
                    'Local team': str(infoNode[2].get()),
                    'Points Local': str(infoNode[3].get()),
                    'Visitor Team': str(infoNode[4].get()),
                    'Points Visitors': str(infoNode[5].get()),
                    'Location': str(infoNode[6].get())
                }