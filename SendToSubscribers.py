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

mymessage = telegram.Emoji.THUMBS_UP_SIGN + " *Aggiornamenti!* " + telegram.Emoji.THUMBS_UP_SIGN + "\n\n" + telegram.Emoji.ROCKET + " Da oggi le biblioteche /metelli e /pinali mostrano il numero di posti liberi, aggiornato in tempo reale - ogni cinque minuti!\n\n" + telegram.Emoji.ROCKET  + " UnipdBot sbarca anche su *Facebook*: presto sarà possibile usarlo anche attraverso *Facebook Messenger!* Per ora, il bot non è raggiungibile pubblicamente; se vuoi provarlo, contatta @mikexine e verrai aggiunto ai tester!\n\n" + telegram.Emoji.ROCKET + " Segui la pagina https://www.facebook.com/UnipdBot-1734334823449262/ per conoscere le ultime novità!\n\nCiao " + telegram.Emoji.HEAVY_BLACK_HEART
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
