#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import arrow
import telegram
import ConfigParser

con = lite.connect('db/logs.db')

start = arrow.get(2015, 11, 18)
end = arrow.utcnow()
last_month = arrow.utcnow().replace(weeks=-2)
user_msg = ""
n_msg = ""


cur = con.cursor()
cur.execute("DELETE FROM log WHERE username = 'mikexine'")
cur.execute("DELETE FROM log WHERE day = '0'")
cur.execute("SELECT COUNT(DISTINCT u_id) FROM log")
users = cur.fetchone()
cur.execute("SELECT COUNT(DISTINCT ch_id) FROM log")
chats = cur.fetchone()
cur.execute('SELECT * FROM log')
rows = cur.fetchall()
cur.execute("DROP TABLE IF EXISTS date")
cur.execute('''CREATE TABLE date (date text, msg_id int)''')
for r in arrow.Arrow.range('day', start, end):
    today = str(r.date())
    cur.execute("SELECT COUNT(*) FROM log WHERE day LIKE ?",
                (today + '%',))
    n = cur.fetchone()[0]
    cur.execute('INSERT INTO date VALUES (?,?)', (today, n))
    if arrow.get(r.date()) > last_month:
        n_msg += "%s, %s\n" % (today, n)
    # print r.date().month
    # print end.month
user_msg += "\n--> %s users in %s chats" % (users[0], chats[0])


# print n_msg
# print user_msg

config = ConfigParser.ConfigParser()
config.read('settings.ini')
token = config.get('main', 'prodtoken')

bot = telegram.Bot(token)
text = n_msg + user_msg
s = bot.sendMessage(chat_id=27002116, text=text)

f = open('oldstats.txt', 'a')
f.write("\n" + str(s))
f.close()
