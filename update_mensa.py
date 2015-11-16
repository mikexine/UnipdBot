#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import requests
import json

mensaList = ['sanfrancesco','piovego','agripolis','acli','belzoni','forcellini','murialdo']

def getcal():
    soup = BeautifulSoup(urllib2.urlopen("http://www.esupd.gov.it/it").read())
    listFull = []
    listPart = []
    listCal = []
    p = 0
    for i in soup.find_all("td"):
        listFull.append(str(i))
    for x in range(7):
        listPart.append(listFull[p])
        listPart.append(listFull[p+1])
        p += 4

    for x in range(len(listPart)):
        if 'open' in listPart[x]:
            listCal.append('Aperto')
        else:
            listCal.append('Chiuso')
    return listCal

def getmenu(mid):
    mensaid = '0'+str(mid)
    soup = BeautifulSoup(urllib2.urlopen("http://www.esupd.gov.it/it/Pagine/Menu.aspx?idmenu=ME_"+mensaid).read())
    completo = {"primo":[],"secondo":[],"contorno":[],"dessert":[]}
    menu = []
    for i in soup.find_all("h2"):
        portata = i.text.split()[0].lower()
        for j in i.next_siblings:
            if j.name == "h2": break
            if j.name == "ul":
                a = str(j)
                menu+=(a.split("<li>"))
                for piatto in range(len(menu)):
                    if "h3" in menu[piatto]:
                        menu[piatto] = menu[piatto].replace('<span style="visibility:hidden">:</span>', ' ')
                        txt = menu[piatto][4:].split("<")[0]
                        completo[portata].append(txt)
            menu = []
    for key in completo:
        if completo[key] == []:
            completo[key] = ['Non disponibile, errore su www.esupd.gov.it o mensa chiusa.']
    return completo

r = requests.get("http://unipd.xyz/mensa", timeout=30)
data = r.json()

mensaDict = data[0]['mensa']
mensaID = data[0]['id']
print mensaID

cal = getcal()

a = 0

for x in range(7):
    mensaDict[mensaList[x]]['calendario']['pranzo'] = cal[a]
    mensaDict[mensaList[x]]['calendario']['cena'] = cal[a+1]
    a += 2


for x in range(7):
    mensaDict[mensaList[x]]['menu'] = getmenu(x+1)
    print x

data[0]['mensa'] = mensaDict
r = requests.put("http://unipd.xyz/mensa/"+mensaID, data=json.dumps(data[0]), timeout=30)
print r.json()
