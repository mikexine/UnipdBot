#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arrow
import requests
import sqlite3
import pickledb
from geopy.distance import vincenty
import datetime



HEADERS = {
    'content-type': 'application/json'
    }

URL = 'http://localhost:8000/api/unipd/'

HOME = """
Seleziona un comando dalla tastiera!
"""
BOTINFO = """
I dati sulle mense sono ottenuti automaticamente dal sito dell'ESU di Padova.
@UnipdBot è promosso e sponsorizzato da @udupadova e sviluppato da @mikexine. 
*Lascia una recensione*, cercaci su @storebot!
Per qualunque problema o suggerimento, scrivi a @mikexine qua su Telegram!
Vuoi dare una mano? Visita `unidata.xyz` o scrivi a `@mikexine`
"""

SELEZIONA = "Seleziona una voce dalla tastiera!"


def home():
    markup = [['/mensa', '/aulastudio'],
              ['/biblioteca', '/udupadova'],
              ['/diritto_studio', '/botinfo']]
    return HOME, markup


def mensa():
    markup = [["/sanfrancesco", "/piovego"],
              ["/agripolis", "/acli"],
              ["/belzoni", "/murialdo"],
              ["/forcellini", "/home"]]
    return SELEZIONA, markup


def aulastudio():
    markup = [["/jappelli", "/pollaio"],
              ["/titolivio", "/galilei"],
              ["/marsala", "/viavenezia"],
              ["/vbranca", "/reset"],
              ["/home"]]
    return SELEZIONA, markup


def biblioteca():
    markup = [["/bibliodiritto", "/filosofia", "/ingegneria"],
              ["/someda", "/maldura", "/matematica"],
              ["/storia", "/metelli", "/pinali"],
              ["/caborin", "/cuzabarella", "/universitaria"],
              ["/bibliochimica", "/agribiblio"],
              ["/bibliogeo", "/bibliofarmacia"],
              ["/home"]]
    return SELEZIONA, markup


def dirittostudio():
    markup = [["/borse", "/tasse"],
              ["/200ore", "/informami"],
              ["/home"]]
    return HOME, markup


def udupadova():
    markup = [["/faqlibretto", "/erasmus"],
              ["/controguida", "/cambiocorso"],
              ["/assembleaudu", "/sedeudu"],
              ["/home"]]
    return SELEZIONA, markup


def botInfo():
    return BOTINFO, [['/home']]


def commandList():
    # data = requests.get(URL + 'mensa/', headers=HEADERS).json()
    mList = []
    for key in requests.get(URL + 'mensa/', headers=HEADERS).json():
        mList.append(key)
    mList.remove('last_update')
    for key in requests.get(URL + 'aulastudio/', headers=HEADERS).json():
        mList.append(key)
    for key in requests.get(URL + 'biblioteca/', headers=HEADERS).json():
        mList.append(key)
    for key in requests.get(URL + 'udupadova/', headers=HEADERS).json():
        mList.append(key)
    for key in requests.get(URL + 'dirittostudio/', headers=HEADERS).json():
        mList.append(key)
    return mList


def replier(command):
    db = pickledb.load('db/unipdbot.pickledb', False)
    reply = db.get(command)['text']
    keyboard = db.get(command)['keyboard']
    try:
        coord = db.get(command)['coord']
        lat = coord['lat']
        lon = coord['lon']
    except:
        lat = None
        lon = None
    return reply, keyboard, lat, lon


def position(usrCoord):
    markup = []
    distDict = {'mensa': {}, 'aulastudio': {}, 'biblioteca': {}}
    tmp = distDict
    today = str(datetime.datetime.today().weekday())

    mensa = requests.get(URL + 'mensa/', headers=HEADERS).json()
    del mensa['last_update']
    for key in mensa:
        pranzo = mensa[key]['calendario']['pranzo']
        cena = mensa[key]['calendario']['cena']
        if cena == 1 or pranzo == 1:
            distDict['mensa'][key] = mensa[key]['coord']

    biblioteca = requests.get(URL + 'biblioteca/', headers=HEADERS).json()
    for key in biblioteca:
        if biblioteca[key]['orari'][today] != '':
            distDict['biblioteca'][key] = biblioteca[key]['coord']

    aulastudio = requests.get(URL + 'aulastudio/', headers=HEADERS).json()
    for key in aulastudio:
        if aulastudio[key]['orari'][today] != '':
            distDict['aulastudio'][key] = aulastudio[key]['coord']

    for key in distDict:
        for i in distDict[key]:
            lat = distDict[key][i]['lat']
            lon = distDict[key][i]['lon']
            tmp[key][i] = vincenty((usrCoord['latitude'],
                                    usrCoord['longitude']),
                                   (lat, lon)).kilometers

    nearMensa = min(tmp['mensa'], key=tmp['mensa'].get)
    nearAula = min(tmp['aulastudio'], key=tmp['aulastudio'].get)
    nearBiblio = min(tmp['biblioteca'], key=tmp['biblioteca'].get)

    nearMensaDist = str(round(float(tmp['mensa'][nearMensa]), 4))
    nearAulaDist = str(round(float(tmp['aulastudio'][nearAula]), 4))
    nearBiblioDist = str(round(float(tmp['biblioteca'][nearBiblio]), 4))

    line1 = "- `Mensa` più vicina, aperta oggi: *%s*, distante _%s_ km.\n\n" %\
        (mensa[nearMensa]['nome'].encode("utf-8"),
         nearMensaDist.encode("utf-8"))
    line2 = "- `Aula studio` più vicina, aperta oggi: *%s*, distante _%s_ km.\n\n" %\
        (aulastudio[nearAula]['nome'].encode("utf-8"),
         nearAulaDist.encode("utf-8"))
    line3 = "- `Biblioteca` più vicina, aperta oggi: *%s*, distante _%s_ km.\n\n" %\
        (biblioteca[nearBiblio]['nome'].encode("utf-8"),
         nearBiblioDist.encode("utf-8"))
    reply = line1 + line2 + line3

    markup.append(['/'+nearMensa.encode("utf-8")])
    markup.append(['/'+nearAula.encode("utf-8")])
    markup.append(['/'+nearBiblio.encode("utf-8")])

    return reply, markup


def writedb(mdict):
    a, b, c, d, e, f, g, h = [0, 0, 0, 0, 0, 0, 0, 0]

    con = sqlite3.connect("db/logs.db")

    try:
        a = mdict["message_id"]
    except:
        pass

    try:
        b = mdict["from"]["id"]
    except:
        pass

    try:
        c = mdict["from"]["username"]
    except:
        pass

    try:
        d = mdict["from"]["first_name"]
    except:
        pass

    try:
        e = mdict["from"]["last_name"]
    except:
        pass

    try:
        f = mdict["text"]
    except:
        pass

    try:
        g = mdict["chat"]["id"]
    except:
        pass
    try:
        h = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss:SSS ZZ')
    except:
        pass

    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO log VALUES (?,?,?,?,?,?,?,?)", (a, b, c, d, e, f, g, h))
