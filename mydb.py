#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickledb
import requests
from time import sleep

url = "http://unipd.xyz/"

# getting keyboardcommands
db = pickledb.load('db/commandsDB.db', False)
r = requests.get(url + 'commands', timeout=30)
data = r.json()
for key in range(len(data)):
    cd = {
        'text': data[key]['text'],
        'keyboard': data[key]['keyboard'],
        'coord': None}
    db.set(data[key]['command'], cd)
db.dump()

r = requests.get(url + 'mensa', timeout=30)
data = r.json()
mensaDict = data[1]['mensa']
sleep(1)
lastUpdate = str(data[0]['mensa']['last_update'])
for key in mensaDict:
    menuDict = {'primo': "", 'secondo': "", 'contorno': "", 'dessert': ""}
    orari = mensaDict[key]['orari']
    indirizzo = mensaDict[key]['indirizzo']
    calendario = 'Pranzo: ' + mensaDict[key]['calendario']['pranzo'] +\
        '\nCena: ' + mensaDict[key]['calendario']['cena']
    telefono = mensaDict[key]['telefono']
    coord = mensaDict[key]['coord']
    for mkey in mensaDict[key]['menu']:
        for piatto in mensaDict[key]['menu'][mkey]:
            menuDict[mkey] += piatto + '\n'
    txtmenu = ' -- PRIMO --\n' + menuDict['primo'] +\
              ' -- SECONDO --\n' + menuDict['secondo'] + \
              ' -- CONTORNO --\n' + menuDict['contorno'] +\
              ' -- DESSERT --\n' + menuDict['dessert']
    reply = 'Orari: %s\nIndirizzo: %s\nTelefono: %s\n\nUltimo aggiornamento: %s\n\n%s\n\n%s' % \
            (orari, indirizzo, telefono, lastUpdate, calendario, txtmenu)
    cd = {
        'text': reply,
        'coord': mensaDict[key]['coord'],
        'keyboard': [
            ['/mensa'],
            ['/home']]}
    db.set(key, cd)
db.dump()


r = requests.get(url + 'aulastudio', timeout=30)
data = r.json()
asDict = data[0]['aulastudio']
for key in asDict:
    orari = asDict[key]['orario']
    indirizzo = asDict[key]['indirizzo']
    telefono = asDict[key]['tel']
    posti = asDict[key]['posti']
    coord = asDict[key]['coord']
    reply = 'Posti: %s\nIndirizzo: %s\nTelefono: %s\n -- Orari: -- \n%s\n' % \
        (posti, indirizzo, telefono, orari)
    cd = {
        'text': reply,
        'coord': asDict[key]['coord'],
        'keyboard': [
            ['/aulastudio'],
            ['/home']]}
    db.set(key, cd)
db.dump()
sleep(1)

r = requests.get(url + 'biblioteca', timeout=30)
data = r.json()
asDict = data[0]['biblioteca']
for key in asDict:
    orari = asDict[key]['orario']
    nome = asDict[key]['nome']
    indirizzo = asDict[key]['indirizzo']
    coord = asDict[key]['coord']
    reply = '%s\nIndirizzo: %s\n -- Orari: -- \n%s\n' % \
        (nome, indirizzo, orari)
    cd = {
        'text': reply,
        'coord': asDict[key]['coord'],
        'keyboard': [
            ['/biblioteca'],
            ['/home']]}
    db.set(key, cd)
db.dump()
sleep(1)


menu = db.get('help')
db.set('home', menu)
db.dump()


### GETTING DATA FOR NEAR POINTS OF INTEREST ####

# getting mensa data
db = pickledb.load('db/mensaDB.db', False)
r = requests.get(url + 'mensa', timeout=30)
data = r.json()
mensaDict = data[1]['mensa']
sleep(1)
lastUpdate = str(data[0]['mensa']['last_update'])
for key in mensaDict:
    menuDict = {'primo': "", 'secondo': "", 'contorno': "", 'dessert': ""}
    orari = mensaDict[key]['orari']
    indirizzo = mensaDict[key]['indirizzo']
    calendario = 'Pranzo: ' + mensaDict[key]['calendario']['pranzo'] +\
        '\nCena: ' + mensaDict[key]['calendario']['cena']
    telefono = mensaDict[key]['telefono']
    coord = mensaDict[key]['coord']
    for mkey in mensaDict[key]['menu']:
        for piatto in mensaDict[key]['menu'][mkey]:
            menuDict[mkey] += piatto + '\n'
    txtmenu = ' -- PRIMO --\n' + menuDict['primo'] +\
              ' -- SECONDO --\n' + menuDict['secondo'] + \
              ' -- CONTORNO --\n' + menuDict['contorno'] +\
              ' -- DESSERT --\n' + menuDict['dessert']
    reply = 'Orari: %s\nIndirizzo: %s\nTelefono: %s\n\nUltimo aggiornamento: %s\n\n%s\n\n%s' % \
            (orari, indirizzo, telefono, lastUpdate, calendario, txtmenu)
    cd = {
        'text': reply,
        'coord': mensaDict[key]['coord'],
        'keyboard': [
            ['/mensa'],
            ['/home']]}
    db.set(key, cd)
db.dump()


db = pickledb.load('db/aulastudioDB.db', False)
r = requests.get(url + 'aulastudio', timeout=30)
data = r.json()
asDict = data[0]['aulastudio']
for key in asDict:
    orari = asDict[key]['orario']
    indirizzo = asDict[key]['indirizzo']
    telefono = asDict[key]['tel']
    posti = asDict[key]['posti']
    coord = asDict[key]['coord']
    reply = 'Posti: %s\nIndirizzo: %s\nTelefono: %s\n -- Orari: -- \n%s\n' % \
        (posti, indirizzo, telefono, orari)
    cd = {'text': reply, 'coord': asDict[key]['coord']}
    db.set(key, cd)
db.dump()
sleep(1)

db = pickledb.load('db/biblioDB.db', False)
r = requests.get(url + 'biblioteca', timeout=30)
data = r.json()
asDict = data[0]['biblioteca']
for key in asDict:
    nome = asDict[key]['nome']
    orari = asDict[key]['orario']
    indirizzo = asDict[key]['indirizzo']
    coord = asDict[key]['coord']
    reply = '%s\nIndirizzo: %s\n -- Orari: -- \n%s\n' % \
        (nome, indirizzo, orari)
    cd = {'text': reply, 'coord': asDict[key][
        'coord'], 'nome': asDict[key]['nome']}
    db.set(key, cd)
db.dump()
sleep(1)
