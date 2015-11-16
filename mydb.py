#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickledb
import requests
import json
from time import sleep


url = "http://unipd.xyz/"



## getting textcommands
db = pickledb.load('textcommandsDB.db', False)
r = requests.get(url+'textcommands', timeout=30)
data = r.json()
for key in range(len(data)):
    db.set(data[key]['command'],data[key]['text'])
db.dump()


# getting keyboardcommands
db = pickledb.load('keyboardcommandsDB.db', False)
r = requests.get(url+'keyboardcommands', timeout=30)
data = r.json()
for key in range(len(data)):
    cd = {'text':data[key]['text'],'keyboard':data[key]['keyboard']}
    db.set(data[key]['command'],cd)
db.dump()

db = pickledb.load('mensaDB.db', False)

r = requests.get(url+'mensa', timeout=30)
data = r.json()
mensaDict = data[0]['mensa']
sleep(1)



for key in mensaDict:
    menuDict = {'primo':"",'secondo':"",'contorno':"", 'dessert':""}
    orari = mensaDict[key]['orari']
    indirizzo = mensaDict[key]['indirizzo']
    calendario = 'Pranzo: '+mensaDict[key]['calendario']['pranzo']+'\nCena: '+mensaDict[key]['calendario']['cena']
    telefono = mensaDict[key]['telefono']
    coord = mensaDict[key]['coord']
    for mkey in mensaDict[key]['menu']:
        for piatto in mensaDict[key]['menu'][mkey]:
            menuDict[mkey] += piatto+'\n'

    txtmenu = ' -- PRIMO --\n'+menuDict['primo'] +' -- SECONDO --\n'+menuDict['secondo'] + \
            ' -- CONTORNO --\n'+menuDict['contorno'] +' -- DESSERT --\n'+menuDict['dessert']

    reply = 'Orari: %s\nIndirizzo: %s\nTelefono: %s\n%s\n\n%s' % (orari, indirizzo, telefono, calendario, txtmenu)
    cd = {'text':reply, 'coord' : mensaDict[key]['coord']}
    db.set(key, cd)
    

db.dump()




# for key in range(len(data)):
#     mensacurr = data[key]['command']
#     orari = data[key]['orari']
#     indirizzo = data[key]['indirizzo']
#     telefono = data[key]['telefono']
#     menucurr = menu[mensacurr]
#     apertura = 'Pranzo: '+mensacal[0]['calendario'][mensacurr]['pranzo']+' - Cena: '+mensacal[0]['calendario'][mensacurr]['cena']

#     text = "Orari: %s\nIndirizzo: %s\n Telefono: %s\n Apertura: %s\n Menu: %s" % (orari, indirizzo, telefono, apertura, menucurr)
#     #print text
#     cd = {'text':text, 'coord' : data[key]['coord']}
#     db.set(mensacurr, cd)

#     # cd = {'text':data[key]['text'],'keyboard':data[key]['keyboard']}
#     # db.set(data[key]['command'],cd)




# db.dump()

# # getting aulastudiocommands



