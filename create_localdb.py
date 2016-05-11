#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import pickledb
from time import sleep
import ConfigParser
from telegram import Bot, ParseMode

config = ConfigParser.ConfigParser()
config.read('settings.ini')

token = str(config.get('main', 'token'))
ch_id = "27002116"
starter = Bot(token=token)
txt = "Updating local unipdbot database"
starter.sendMessage(ch_id, text=txt)

HEADERS = {'content-type': 'application/json'}
URL = str(config.get('main', 'api'))

db = pickledb.load('db/unipdbot.pickledb', False)

mensa = requests.get(URL + 'mensa/', headers=HEADERS).json()
del mensa['last_update']
for key in mensa:
    if mensa[key]['calendario']['pranzo'] == 1:
        pranzo = True
    else:
        pranzo = False
    if mensa[key]['calendario']['cena'] == 1:
        cena = True
    else:
        cena = False

    if pranzo and cena:
        tmp = "oggi è *aperta* sia a pranzo che a cena"
    elif pranzo and not cena:
        tmp = "oggi è *aperta* solo a pranzo"
    elif cena and not pranzo:
        tmp = "oggi è aperta solo a cena"

    if mensa[key]['menu']['primo'][0] == "Menu non pubblicato su www.esupd.gov.it/":
        menu = ""
    elif mensa[key]['menu']['primo'][0] == "Niente menu, errore su www.esupd.gov.it/":
        menu = ""
    else:
        menu = "\n_PRIMO:_ %s\n_SECONDO:_ %s\n_CONTORNO:_ %s\n_DESSERT:_ %s" % \
               (', '.join(mensa[key]['menu']['primo']),
                ', '.join(mensa[key]['menu']['secondo']),
                ', '.join(mensa[key]['menu']['contorno']),
                ', '.join(mensa[key]['menu']['dessert']))

    if not pranzo and not cena:
        text = '*Mensa %s*\nIn %s.\nOggi la mensa è *chiusa*.\n' % \
                (mensa[key]['nome'].encode("utf-8"),
                 mensa[key]['indirizzo'].encode("utf-8"))
        mensa[key]['coord']['lat'] = None
        mensa[key]['coord']['lon'] = None
    else:
        text = '*Mensa %s*\nIn %s, %s con orario: *%s*. \n' % \
                (mensa[key]['nome'].encode("utf-8"),
                 mensa[key]['indirizzo'].encode("utf-8"),
                 tmp,
                 mensa[key]['orari'].encode("utf-8"))
        text = text + menu.encode("utf-8")

    db.set(key, {'text': text, 'keyboard': [['/mensa'], ['/home']],
                 'coord': mensa[key]['coord']})


print 'sleeping'
sleep(2)

aulastudio = requests.get(URL + 'aulastudio/', headers=HEADERS).json()
for key in aulastudio:
    text = "*Aula %s*\n_Posti:_ %s\nIndirizzo: %s\n_Orari:_ %s.\n" % \
           (aulastudio[key]['nome'].encode("utf-8"),
            aulastudio[key]['posti'].encode("utf-8"),
            aulastudio[key]['indirizzo'].encode("utf-8"),
            aulastudio[key]['orario'].encode("utf-8"))
    db.set(key, {'text': text, 'keyboard': [['/aulastudio'], ['/home']],
                 'coord': aulastudio[key]['coord']})

print 'sleeping'
sleep(2)

biblioteca = requests.get(URL + 'biblioteca/', headers=HEADERS).json()
for key in biblioteca:
    if key == "metelli" or key == "pinali":
        text = "*%s*\nPosti liberi: %s\nIndirizzo: %s\n_Orari:_ %s.\n" % \
           (biblioteca[key]['nome'].encode("utf-8"),
            biblioteca[key]['posti'].encode("utf-8"),
            biblioteca[key]['indirizzo'].encode("utf-8"),
            biblioteca[key]['orario'].encode("utf-8"))

    else:
        text = "*%s*\nIndirizzo: %s\n_Orari:_ %s.\n" % \
               (biblioteca[key]['nome'].encode("utf-8"),
                biblioteca[key]['indirizzo'].encode("utf-8"),
                biblioteca[key]['orario'].encode("utf-8"))
    db.set(key, {'text': text, 'keyboard': [['/biblioteca'], ['/home']],
                 'coord': biblioteca[key]['coord']})

print 'sleeping'
sleep(2)

udupadova = requests.get(URL + 'udupadova/', headers=HEADERS).json()
for key in udupadova:
    db.set(key, {'text': udupadova[key]['text'],
                 'keyboard': udupadova[key]['keyboard']})

print 'sleeping'
sleep(2)

dirittostudio = requests.get(URL + 'dirittostudio/', headers=HEADERS).json()
for key in dirittostudio:
    db.set(key, {'text': dirittostudio[key]['text'],
                 'keyboard': dirittostudio[key]['keyboard']})

db.dump()
