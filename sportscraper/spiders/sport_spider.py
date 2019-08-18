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
            print(self.parseNode("-------------------" + infoNode[0].get().decode("latin-1", "replace") + "---------------"))
            yield {
                    'Event date': self.parseNode((infoNode[0].get())),
                    'Time': self.parseNode((infoNode[1].get())),
                    'Local team': self.parseNode((infoNode[2].get())),
                    'Points Local': self.parseNode((infoNode[3].get())),
                    'Visitor Team': self.parseNode((infoNode[4].get())),
                    'Points Visitors': self.parseNode((infoNode[5].get())),
                    'Location': self.parseNode((infoNode[6].get()))
                }

    def parseNode(self, strNode):
        index = strNode.find("<")
        index2 = strNode.find(">")

        if index == -1:
            return strNode
        else:
            strNodeFixed = strNode[0:index] + strNode[index2+1:]
            return self.parseNode(strNodeFixed)
