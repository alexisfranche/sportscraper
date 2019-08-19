import scrapy
import requests

baseUrl = "https://maps.googleapis.com/maps/api/geocode/json?address="
api_key="AIzaSyAglwogS08ArRJ7rUQu7xu_yGJxr6ZanZI"

class SportSpider(scrapy.Spider):
    name = "sport"
    start_urls = [
        'http://tornades.org/horaire-novice-masculin-a/'
    ]

    #Default method that framework will seek
    def parse(self, response):
        table = response.css("#content > div.entry-content > table:nth-child(1)")
        body = table.css("tbody")
        ctn = body.css("tr")
        dataList = ctn.css("tr")
        dataList.pop(0) #remove table headers
        for data in dataList:
            infoNode = data.css("td")

            #linkLoc = self.parseMapsLink(infoNode[6].css("a::attr(href)").get())

            Address = self.parseMapsLink(infoNode[6].css("a::attr(href)").get())
            if Address is not None:
                info = requests.get(baseUrl + Address + "&key=" +api_key)
                resp_json_payload = info.json()
                print(resp_json_payload)
            latitude = None
            longitude = None

            yield {
                    'Event date': self.parseNode((infoNode[0].get())),
                    'Time': self.parseNode((infoNode[1].get())),
                    'Local team': self.parseNode((infoNode[2].get())),
                    'Points Local': self.parseNode((infoNode[3].get())),
                    'Visitor Team': self.parseNode((infoNode[4].get())),
                    'Points Visitors': self.parseNode((infoNode[5].get())),
                    'Location Name': self.parseNode((infoNode[6].get())),
                    'Location Address': Address,
                    'Latitude': latitude,
                    'Longitude': longitude,
                }

    #Method added to parse text content retrieved (remove tags).
    def parseNode(self, strNode):
        index = strNode.find("<")
        index2 = strNode.find(">")

        if index == -1:
            return strNode
        else:
            strNodeFixed = strNode[0:index] + strNode[index2+1:]
            return self.parseNode(strNodeFixed)

    def parseMapsLink(self, link):
        if link is not None:
            index = link.find("place/")

            if index == -1:
                return None
            else:
                addressTemp = link[index+6:]
                index2 = addressTemp.find("/")
                addressTemp = addressTemp[:index2]
                #address = addressTemp.replace("+", " ")

                return addressTemp
        else:
            return None

