from bs4 import BeautifulSoup
import os
import re
from ruamel.yaml import YAML
import urllib.request as urllib

def getPKMNS():
    baseUrl = 'https://bulbapedia.bulbagarden.net'
    startUrl = '/wiki/Bulbasaur_(Pok%C3%A9mon)'
    url = baseUrl + startUrl

    soup,link = requestPage(url)
    print(link)
    input()

    while link != startUrl and link != '/wiki/%3F%3F%3F_(Pok%C3%A9mon)' and link != '/wiki/Pok%C3%A9mon_(species)':
        url = baseUrl + link
        soup,link = requestPage(url)
        print(link)
        input()

    print('end')

def savePKMN(data,pokemon="Missingno",filePath=os.path.abspath(__file__)[:-10] + "..\\data\\"):
    filePath = filePath + pokemon + ".dex"
    dex = open(filePath,'a+')
    dex.write(data)
    dex.close()

def requestPage(url):
    req = urllib.Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0'
        }
    )
    html = urllib.urlopen(req)
    soup = BeautifulSoup(html,features="html.parser")
    link = soup.body.find_next('a',title=re.compile(r'. \(Pokémon\)'),string='→')

    return soup, link["href"]

    
if __name__ == "__main__":
    print()
    getPKMNS()