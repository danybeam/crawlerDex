from bs4 import BeautifulSoup
import os
import re
from ruamel.yaml import YAML
import urllib.request as urllib

def getPKMNS():
    baseUrl = 'https://bulbapedia.bulbagarden.net'
    #startUrl = '/wiki/Bulbasaur_(Pok%C3%A9mon)'
    #startUrl = '/wiki/Rockruff_(Pok%C3%A9mon)'
    #startUrl = '/wiki/Lycanroc_(Pok%C3%A9mon)'
    startUrl = '/wiki/Eevee_(Pok%C3%A9mon)'
    url = baseUrl + startUrl
    soup,link = requestPage(url)

    while link != startUrl and url[:-30] != '/wiki/%3F%3F%3F_(Pok%C3%A9mon)' and url[:-28] != '/wiki/Pok%C3%A9mon_(species)':
        data = {}
        data["Name"] = getPKMNName(soup)
        data["Base Stats"] = getPKMNBaseStats(soup,data["Name"])
        data["Forms"] = []
        for key in data["Base Stats"].keys():
            data["Forms"].append(str(key))
        data["Types"] = getPKMNTypes(soup)
        data["Abilities"] = getPKMNAbilities(soup)
        data["Evolutions"] = getPKMNEvos(soup,data["Name"])

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

def getPKMNBaseStats(soup,name="Missingno"):
    referenceString = ['HP','Attack','Defense','Sp. Atk', 'Sp. Def', 'Speed']
    stats = {}
    tables = soup.body.find_all('table',style=re.compile(r'background: #......; border-radius: 10px; -moz-border-radius: 10px; -webkit-border-radius: 10px; -khtml-border-radius: 10px; -icab-border-radius: 10px; -o-border-radius: 10px;; border: 3px solid #......; white-space:nowrap'))
    for table in tables:
        form = str(table.previous_sibling.previous_sibling.string)
        if form.endswith("stats"):
            form = name
        stats[form] = {}
        ref_table = table.find_all('tr',style=re.compile(r'text-align:center'))
        counter = 0
        for i in ref_table:
            stats[form][referenceString[counter]] = int(i.find_all('div')[1].string)
            counter += 1
    return dict(stats)

def getPKMNTypes(soup):
    types = soup.body.find_all('a',title=re.compile(r'\(type\)'))[0:2]
    data = [types[0].b.string]
    if types[1].b.string != 'Unknown':
        data.append(types[1].b.string)        
    data = [str(i) for i in data]
    return data

def getPKMNAbilities(soup):
    html1 = soup.body.find_all('a',title=re.compile(r'\(Ability\)'))
    Abilities = dict()
    for item in html1:
        if item.string in Abilities:
            continue
        if item.parent.has_attr("style") and item.parent["style"] == "display: none":
            continue
        if item.parent.small:
            Abilities[str(item.string)] = str(item.parent.small.string).strip()
        else:
            Abilities[str(item.string)] = "Ability"
    return Abilities

def notImage(href):
    return href and not re.compile(r'png').search(href)

# TODO Fix forms for mutli-evos (rockruff, eevee, oddish, etc)
# TODO Fix offset for eevee
def getPKMNEvos(soup,pokemon="Missingno"):
    stepOver = 1
    method = None
    evoName = ''
    evos = {}
    if pokemon == "Eevee":
        stepOver = 8

    table = soup.body.find_all('table',style=re.compile(r'margin:auto; text-align:center; background: #......; border-radius: 10px; -moz-border-radius: 10px; -webkit-border-radius: 10px; -khtml-border-radius: 10px; -icab-border-radius: 10px; -o-border-radius: 10px; border: 3px solid #......;'))[0]
    for evo_table in table:
        evo_table = table.find_all('td')
        for i in range(len(evo_table)):
            #print(table[i])
            if evo_table[i].find_all(string=re.compile(r'[→↓]')):
                method = str(evo_table[i].find_next('a',href=notImage).string)
                evoName = str(evo_table[i+stepOver].find_next('a',title=re.compile(r'Pokémon')).span.string)
                evos[evoName] = method
                print()
    return dict(evos)

def savePKMN(data,pokemon="Missingno",filePath=os.getcwd() + "\\data\\pkmns\\"):
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    yaml = YAML()
    filePath = filePath + pokemon + ".dex"
    dex = open(filePath,'w')
    yaml.dump(data,dex)
    dex.close()
    
if __name__ == "__main__":
    getPKMNS()