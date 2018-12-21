from bs4 import BeautifulSoup
import os
import re
from ruamel.yaml import YAML
import urllib.request as urllib

def getPKMNS():
    baseUrl = 'https://bulbapedia.bulbagarden.net'
    startUrl = '/wiki/Bulbasaur_(Pok%C3%A9mon)'
    savePKMN(startUrl)
    url = baseUrl + startUrl
    stop = False
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

    while link['href'] != startUrl or not stop:
        savePKMN(link['href'])
        url = baseUrl + link['href']
        stop = True
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
    print('end')

def savePKMN(data,filePath=''):
    filePath = os.getcwd
    dex = open(filePath,'a+')
    dex.write(data)
    dex.close()

    
if __name__ == "__main__":
    print()
    print(os.path.dirname(os.path.relpath(__file__)))
    print(os.path.dirname(os.path.abspath(__file__)))
    input()
    getPKMNS()