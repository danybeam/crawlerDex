from bs4 import BeautifulSoup
import os
import re
from ruamel.yaml import YAML
import time
import urllib.request as urllib

def getPKMNS():
    baseUrl = 'https://bulbapedia.bulbagarden.net'
    startUrl = '/wiki/Bulbasaur_(Pok%C3%A9mon)'
    url = baseUrl + startUrl
    soup,link = requestPage(url)

    while link != startUrl and link != '/wiki/%3F%3F%3F_(Pok%C3%A9mon)' and link != '/wiki/Pok%C3%A9mon_(species)':
        PKMNName = getPKMNName(soup)
        PKMNBaseStats = getPKMNBaseStats(soup)
        data = {}
        data["Name"] = PKMNName
        data["Base Stats"] = PKMNBaseStats

        print(data["Name"])
        savePKMN(data,pokemon=str(data['Name']))
        
        url = baseUrl + link
        soup,link = requestPage(url)

    print('end')

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

def getPKMNName(soup):
    name = soup.body.find_next('td',width='50%')
    name = str(name.big.big.b.string) 
    if name[-1] == '♀':
        name = name[:-1] + 'F'
    if name[-1] == '♂':
        name = name[:-1] + 'M'
    return name

def getPKMNBaseStats(soup):
    referenceString = ['HP','Attack','Defense','Sp. Atk', 'Sp. Def', 'Speed']
    counter = 0
    stats = {}
    table = soup.body.find_next('table',style=re.compile(r'background: #......; border-radius: 10px; -moz-border-radius: 10px; -webkit-border-radius: 10px; -khtml-border-radius: 10px; -icab-border-radius: 10px; -o-border-radius: 10px;; border: 3px solid #......; white-space:nowrap'))
    table = table.find_all('tr',style=re.compile(r'text-align:center'))
    for i in table:
        stats[referenceString[counter]] = int(i.find_all('div')[1].string)
        counter += 1
    return dict(stats)
def getPKMNTypes(soup):
    pass

def savePKMN(data,pokemon="Missingno",filePath=os.path.abspath(__file__)[:-10] + "..\\data\\"):
    yaml = YAML()
    filePath = filePath + pokemon + ".dex"
    dex = open(filePath,'w')
    yaml.dump(data,dex)
    dex.close()
    
if __name__ == "__main__":
    print()
    getPKMNS()