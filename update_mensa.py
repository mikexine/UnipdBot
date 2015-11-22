#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import requests
import json
import arrow
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('settings.ini')
auth = config.get('main', 'auth')
headers = {
    'Content-Type': 'application/json',
    'mikexine': auth
}

mensaList = ['sanfrancesco', 'piovego', 'agripolis', 'acli',
             'belzoni', 'forcellini', 'murialdo']
rep = '<span style="visibility:hidden">:</span>'
nomenu = 'Menu non pubblicato su www.esupd.gov.it/'
errmenu = ['Niente menu, errore su www.esupd.gov.it/']


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
        listPart.append(listFull[p + 1])
        p += 4
    for x in range(len(listPart)):
        if 'open' in listPart[x]:
            listCal.append('Aperto')
        else:
            listCal.append('Chiuso')
    return listCal


def getmenu(mid):
    mensaid = '0' + str(mid)
    completo = {"primo": [], "secondo": [], "contorno": [], "dessert": []}
    try:
        url = "http://www.esupd.gov.it/it/Pagine/Menu.aspx?idmenu=ME_"
        soup = BeautifulSoup(urllib2.urlopen(url + mensaid).read())
        menu = []
        for i in soup.find_all("h2"):
            portata = i.text.split()[0].lower()
            for j in i.next_siblings:
                if j.name == "h2":
                    break
                if j.name == "ul":
                    a = str(j)
                    menu += (a.split("<li>"))
                    for piatto in range(len(menu)):
                        if "h3" in menu[piatto]:
                            menu[piatto] = menu[piatto].replace(rep, ' ')
                            txt = menu[piatto][4:].split("<")[0]
                            completo[portata].append(txt)
                menu = []
        for key in completo:
            if completo[key] == []:
                completo[key] = [nomenu]
    except:
        for key in completo:
            completo[key] = errmenu
    return completo

r = requests.get("http://unipd.xyz/mensa", timeout=30)
data = r.json()
mensaDict = data[1]['mensa']
mensaID = data[1]['id']
print mensaID

try:
    cal = getcal()
except:
    cal = None
a = 0

if cal is not None:
    for x in range(7):
        mensaDict[mensaList[x]]['calendario']['pranzo'] = cal[a]
        mensaDict[mensaList[x]]['calendario']['cena'] = cal[a + 1]
        a += 2
else:
    for x in range(7):
        mensaDict[mensaList[x]]['calendario'][
            'pranzo'] = "errore su www.esupd.gov.it/"
        mensaDict[mensaList[x]]['calendario'][
            'cena'] = "errore su www.esupd.gov.it/"
        a += 2

for x in range(7):
    mensaDict[mensaList[x]]['menu'] = getmenu(x + 1)
    print x

data[1]['mensa'] = mensaDict
r = requests.put("http://unipd.xyz/mensa/" + mensaID,
                 data=json.dumps(data[1]), headers=headers, timeout=30)


updateID = data[0]['id']
now = arrow.now('CET').format('HH:mm - DD-MM-YYYY')
print now
data[0]['mensa']['last_update'] = now
print data[0]
r = requests.put("http://unipd.xyz/mensa/" + updateID,
                 data=json.dumps(data[0]), headers=headers, timeout=30)
print r.json()
