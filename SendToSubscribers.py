#!/usr/bin/python
# -*- coding: utf-8 -*-

import telegram
import sys
import ConfigParser
import sqlite3
from time import sleep

sys.stdout = open('log/sendMe.log', "w")

config = ConfigParser.ConfigParser()
config.read('settings.ini')
token = config.get('main', 'token')

mymessage = "Ciao! Sono stato aggiornato, dovrei essere leggermente più veloce! Lo sapevi che puoi anche inviarmi la tua posizione? Saprai subito quale è l'aula studio, la mensa e la biblioteca più vicine a te aperte in questo momento! ;)"

text = mymessage

print 'sending message: ' + text

con = sqlite3.connect("db/logs.db")
cur = con.cursor()
cur.execute('SELECT * FROM log')
rows = cur.fetchall()
users = set([])

for row in rows:
    users.add(str(row[6]))

print users

bot = telegram.Bot(token)

for user in users:
    try:
        bot.sendMessage(chat_id=user, text=text)
        print 'Message sent to: ' + user
        sleep(0.2)
    except telegram.error.TelegramError as e:
        if 'unauthorized' in str(e).lower():
            print 'unauthorized error with user: ' + user
