#!/usr/bin/python
# -*- coding: utf-8 -*-

import telegram
import sys
import ConfigParser
import sqlite3
from time import sleep

# sys.stdout = open('log/sendMe.log', "w")

config = ConfigParser.ConfigParser()
config.read('settings.ini')
token = config.get('main', 'token')

mymessage = "*ELEZIONI STUDENTESCHE 2016*\n\nIl *18 e il 19 maggio* potrai scegliere i tuoi nuovi rappresentanti nei Consigli di Corso, negli Organi Maggiori e nel Consiglio Nazionale degli Studenti Universitari.\n\nCandidati con *UDU - Studenti Per*! Il termine ultimo per le candidature è il *5 aprile*. Sei interessato, ma hai dubbi o perplessità? Puoi contattare @francocorti92 o @alejo91 :)"
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
        bot.sendMessage(chat_id=user, text=text, parse_mode=telegram.ParseMode.MARKDOWN)
        print 'Message sent to: ' + user
        sleep(0.2)
    except telegram.error.TelegramError as e:
        if 'unauthorized' in str(e).lower():
            print 'unauthorized error with user: ' + user
