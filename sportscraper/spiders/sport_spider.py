import scrapy
import requests
from geopy.geocoders import Nominatim

baseUrl = "https://maps.googleapis.com/maps/api/geocode/json?address="
api_key="AIzaSyD0eMKjYpqtMwsXFFttIPxdDFAYkGlQEeQ"

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
            latitude = None
            longitude = None
            Address = self.parseMapsLink(infoNode[6].css("a::attr(href)").get())
            print(Address)
            if Address is not None:
                geolocator = Nominatim(user_agent="sportscraper")
                location = geolocator.geocode(Address)
                if location is not None:
                    latitude = str(location.raw["lat"])
                    longitude = str(location.raw["lon"])

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
                    'Google Maps Link': infoNode[6].css("a::attr(href)").get(),
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
                address = addressTemp.replace("+", " ")
                index3 = self.findKey(address, ",", 1)#address.find(",")
                if index3 == -1:
                    return self.handleSpecChar(address)
                else:
                    address = address[:index3]
                    return self.handleSpecChar(address)
        else:
            return None

    def handleSpecChar(self, address):

        index = address.find("%C3%")

        if index == -1:
            return address
        else:
            address = address[:index] + "e" + address[index+6:]
            return address

    def findKey(self, haystack, needle, n):
        parts = haystack.split(needle, n + 1)
        if len(parts) <= n + 1:
            return -1
        return len(haystack) - len(parts[-1]) - len(needle)
