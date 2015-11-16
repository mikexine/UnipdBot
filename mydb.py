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

db = pickledb.load('mensacommandsDB.db', False)

r = requests.get(url+'mensacommands', timeout=30)
data = r.json()
#print data
sleep(1)

r = requests.get(url+'mensacalendario', timeout=30)
mensacal = r.json()
#print mensacal
sleep(1)

r = requests.get(url+'mensamenu', timeout=30)
mensamenu = r.json()

menu = {
    "sanfrancesco":"",
    "piovego":"",
    "agripolis":"",
    "acli":"",
    "belzoni":"",
    "forcellini":"",
    "murialdo":""
}

testoprimo = ''
testosecondo = ''
testocontorno = ''
testodessert = ''

for mensa in range(len(mensamenu)):

    m = mensamenu[mensa]['mensa']
    # print '-----------'
    # print m
    

    for piatto in range(len(mensamenu[mensa]['menu']['primo'])):
        primo = mensamenu[mensa]['menu']['primo'][piatto]
        testoprimo = testoprimo + '\n' + primo
    # print testoprimo

    for piatto in range(len(mensamenu[mensa]['menu']['secondo'])):
        secondo = mensamenu[mensa]['menu']['secondo'][piatto]
        testosecondo = testosecondo + '\n' + secondo
    # print testosecondo

    for piatto in range(len(mensamenu[mensa]['menu']['contorno'])):
        contorno = mensamenu[mensa]['menu']['contorno'][piatto]
        testocontorno = testocontorno + '\n' + contorno
    # print testocontorno

    for piatto in range(len(mensamenu[mensa]['menu']['dessert'])):
        dessert = mensamenu[mensa]['menu']['dessert'][piatto]
        testodessert = testodessert + '\n' + dessert
    # print testodessert

    menu[m] = 'PRIMO'+testoprimo + '\n\nSECONDO'+ testosecondo +'\n\nCONTORNO'+ testocontorno +'\n\nDESSERT'+ testodessert

    testoprimo = ''
    testosecondo = ''
    testocontorno = ''
    testodessert = ''
    # print '-----------'


for key in range(len(data)):
    mensacurr = data[key]['command']
    orari = data[key]['orari']
    indirizzo = data[key]['indirizzo']
    telefono = data[key]['telefono']
    menucurr = menu[mensacurr]
    apertura = 'Pranzo: '+mensacal[0]['calendario'][mensacurr]['pranzo']+' - Cena: '+mensacal[0]['calendario'][mensacurr]['cena']

    text = "Orari: %s\nIndirizzo: %s\n Telefono: %s\n Apertura: %s\n Menu: %s" % (orari, indirizzo, telefono, apertura, menucurr)
    #print text
    cd = {'text':text, 'coord' : data[key]['coord']}
    db.set(mensacurr, cd)

    # cd = {'text':data[key]['text'],'keyboard':data[key]['keyboard']}
    # db.set(data[key]['command'],cd)




db.dump()

# # getting aulastudiocommands



