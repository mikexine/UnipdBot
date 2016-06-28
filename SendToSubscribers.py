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

mymessage = "Ciao! Hai un momento libero?\n\n" + telegram.Emoji.PENCIL + " Compila il questionario Io Studente, bastano 5 minuti! Un modo per fotografare la condizione materiale degli studenti universitari del nostro paese, dagli alloggi ai trasporti passando per il costo della vita.\n\n" + telegram.Emoji.PENCIL + " Il link al questionario è questo: https://goo.gl/mlck4s \n\nGrazie, e in bocca al lupo per la sessione! " + telegram.Emoji.HEAVY_BLACK_HEART
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
