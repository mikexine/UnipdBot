#!/usr/bin/python
# -*- coding: utf-8 -*-

import telegram
import sqlite3
import pickledb
from geopy.distance import vincenty
import arrow

con = sqlite3.connect("db/logs.db")


class pyUniPd:

    def __init__(self):
        pass

    @classmethod
    def commandlist(self, db):
        mydb = pickledb.load(db, False)
        commands = []
        for command in mydb.getall():
            commands.append(command)
        return commands

    @classmethod
    def dict_factory(self, curs, row):
        d = {}
        for idx, col in enumerate(curs.description):
            d[col[0]] = row[idx]
        return d

    @classmethod
    def writedb(self, mdict):
        a, b, c, d, e, f, g, h = [0, 0, 0, 0, 0, 0, 0, 0]

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
            cur.execute("INSERT INTO log VALUES (?,?,?,?,?,?,?,?)",
                        (a, b, c, d, e, f, g, h))

    def sendNearPOI(self, bot, chat_id, pos):
        io = (pos['latitude'], pos['longitude'])
        distDict = {}
        db = pickledb.load('db/mensaDB.db', False)
        for key in db.getall():
            a = db.get(key)
            mensaCoord = (a['coord']['lat'], a['coord']['lon'])
            distDict[key] = vincenty(io, mensaCoord).kilometers
        MensaNearPOI = min(distDict, key=distDict.get)
        km = str(round(float(distDict[MensaNearPOI]), 4))
        prettyNearPOI = str(MensaNearPOI).title()
        if prettyNearPOI == 'Sanfrancesco':
            prettyNearPOI = 'San Francesco'
        textMensa = 'Mensa più vicina: ' + str(prettyNearPOI) + \
                    ', distanza: ' + str(km) + ' km' + \
                    '. \nPer maggiori informazioni: /' + str(MensaNearPOI)

        io = (pos['latitude'], pos['longitude'])
        distDict = {}
        db = pickledb.load('db/aulastudioDB.db', False)
        for key in db.getall():
            a = db.get(key)
            asCoord = (a['coord']['lat'], a['coord']['lon'])
            distDict[key] = vincenty(io, asCoord).kilometers
        AsNearPOI = min(distDict, key=distDict.get)
        km = str(round(float(distDict[AsNearPOI]), 4))
        prettyNearPOI = str(AsNearPOI).title()
        if prettyNearPOI == 'Viavenezia':
            prettyNearPOI = 'Via Venezia'
        elif prettyNearPOI == 'Titolivio':
            prettyNearPOI = 'Tito Livio'
        elif prettyNearPOI == 'Vbranca':
            prettyNearPOI = 'Vittore Branca'
        elif prettyNearPOI == 'Reset':
            prettyNearPOI = 'Circolo Reset'
        textAS = '\n\nAula studio più vicina: ' + str(prettyNearPOI) + \
            ', distanza: ' + str(km) + ' km' + \
            '. \nPer maggiori informazioni: /' + str(AsNearPOI)

        distDict = {}
        db = pickledb.load('db/biblioDB.db', False)
        for key in db.getall():
            a = db.get(key)
            biblioCoord = (a['coord']['lat'], a['coord']['lon'])
            distDict[key] = vincenty(io, biblioCoord).kilometers
        biblioNearPOI = min(distDict, key=distDict.get)
        km = str(round(float(distDict[biblioNearPOI]), 4))
        prettyNearPOI = db.get(biblioNearPOI)['nome']
        textBiblio = '\n\nBiblioteca più vicina: ' + str(prettyNearPOI) + \
            ', distanza: ' + str(km) + ' km' + \
            '. \nPer maggiori informazioni: /' + str(biblioNearPOI)

        text = textMensa + textAS + textBiblio
        markup = [['/' + MensaNearPOI, '/' + AsNearPOI],
                  ['/' + biblioNearPOI, '/home']]
        reply_markup = telegram.ReplyKeyboardMarkup(markup)
        bot.sendMessage(chat_id=chat_id, text=text, reply_markup=reply_markup)

    def reply(self, bot, update, message, command, chat_id):
        commandsDB = pickledb.load('db/commandsDB.db', False)
        pyUniPd.writedb(update.message.to_dict())
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        reply = commandsDB.get(command)['text']
        markup = commandsDB.get(command)['keyboard']
        reply_markup = telegram.ReplyKeyboardMarkup(markup)
        bot.sendMessage(chat_id=chat_id, text=reply,
                        reply_markup=reply_markup)
        if commandsDB.get(command)['coord'] is not None:
            lat = commandsDB.get(command)['coord']['lat']
            lon = commandsDB.get(command)['coord']['lon']
            bot.sendLocation(chat_id=chat_id, latitude=lat, longitude=lon)
        else:
            pass

    def adminStats(self, bot, update, message, command, chat_id):
        pyUniPd.writedb(update.message.to_dict())
        connection = sqlite3.connect("db/logs.db")
        connection.row_factory = pyUniPd.dict_factory
        curs = connection.cursor()
        curs.execute("select * from log")
        results = curs.fetchall()
        connection.close()
        userList = []
        nMsg = 0
        for i in range(len(results)):
            nMsg += 1
            user = results[i]['first_name'] + '-' + \
                results[i]['last_name'] + '-' + results[i]['username']
            if user not in userList:
                userList.append(user)
        uIDList = []
        for i in range(len(results)):
            chat = results[i]['u_id']
            if chat not in uIDList:
                uIDList.append(chat)
        nMsgUser = {}
        for us in uIDList:
            nMsgUser[us] = 0
        for i in range(len(results)):
            nMsgUser[results[i]['u_id']] += 1
        uDict = {}
        for key in nMsgUser:
            uDict[key] = {
                'nMsg': nMsgUser[key],
                'name': ''}
        for i in range(len(results)):
            uDict[results[i]['u_id']]['name'] = results[i]['first_name'] + \
                '~' + results[i]['last_name'] + ' | @' + results[i]['username']
        out = ''
        out = out + 'Number of single users: ' + str(len(userList) - 1) + '\n'
        out = out + 'Number of single messages exchanged: ' + str(nMsg) + '\n'
        out = out + 'Number of single messages sent: ' + str(nMsg / 2) + '\n'
        out = out + '\n -- TOP 20 USERS -- \n'
        top = []
        for w in sorted(uDict, key=uDict.get, reverse=True):
            tx = uDict[w]['name'] + ' | nMsg: ' + str(uDict[w]['nMsg'])
            top.append(tx)
        for i in range(20):
            out = out + str(i + 1) + ' ' + top[i] + '\n\n'
        reply = out
        bot.sendMessage(chat_id=chat_id, text=reply)
