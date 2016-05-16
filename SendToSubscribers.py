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

mymessage = telegram.Emoji.NEWSPAPER + " *Elezioni 2016!* " + telegram.Emoji.NEWSPAPER + "\n\n" + telegram.Emoji.PENCIL + " Il 18 e il 19 maggio, gli studenti dell'Università di Padova saranno chiamati ad eleggere i rappresentanti per il loro corso, per il CUS, il CDA e il Senato Accademico, il CDA dell'Esu e il CNSU.\n\n" + telegram.Emoji.PENCIL + " Informati bene sulle liste, sui programmi e sui candidati, scegli chi preferisci; la cosa più importante è andare a votare! "
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
