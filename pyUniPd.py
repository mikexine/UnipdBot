#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import telegram
import sqlite3
import time
import pickledb
from geopy.distance import vincenty

con = sqlite3.connect("db/logs.db")


class pyUniPd:

    def __init__(self):
        pass

    @classmethod
    def commandlist(self,db):
        mydb = pickledb.load(db, False)
        commands = []
        for command in mydb.getall():
            commands.append(command)
        return commands

    @classmethod
    def writedb(self, mdict):
        a, b, c, d, e, f, g, h = [0,0,0,0,0,0,0,0]

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
            h = (datetime.datetime.fromtimestamp(int(mdict["date"]))
                .strftime("%Y-%m-%d %H:%M:%S"))
        except:
            pass

        with con: 
            cur = con.cursor()
            cur.execute("INSERT INTO log VALUES (?,?,?,?,?,?,?,?)", 
                       (a, b, c, d, e, f, g, h))

    def sendNearPOI(self,bot,chat_id,pos):
        io = (pos['latitude'],pos['longitude'])
        distDict = {}
        db = pickledb.load('mensaDB.db',False)
        for key in db.getall():
            a = db.get(key)
            mensaCoord = (a['coord']['lat'], a['coord']['lon'])
            distDict[key] = vincenty(io, mensaCoord).kilometers
        nearPOI = min(distDict, key=distDict.get)
        km = str(round(float(distDict[nearPOI]), 4))
        prettyNearPOI = str(nearPOI).title()
        if prettyNearPOI == 'Sanfrancesco':
            prettyNearPOI = 'San Francesco'
        textMensa = 'Mensa più vicina: '+str(prettyNearPOI) + \
                    ', distanza: '+str(km)+' km'+ \
                    '. \nPer maggiori informazioni: /'+str(nearPOI)

        io = (pos['latitude'],pos['longitude'])
        distDict = {}
        db = pickledb.load('aulastudioDB.db',False)
        for key in db.getall():
            a = db.get(key)
            asCoord = (a['coord']['lat'], a['coord']['lon'])
            distDict[key] = vincenty(io, asCoord).kilometers
        nearPOI = min(distDict, key=distDict.get)
        km = str(round(float(distDict[nearPOI]), 4))
        prettyNearPOI = str(nearPOI).title()
        if prettyNearPOI == 'Viavenezia':
             prettyNearPOI = 'Via Venezia'
        elif prettyNearPOI == 'Titolivio':
             prettyNearPOI = 'Tito Livio'
        elif prettyNearPOI == 'Vbranca':
             prettyNearPOI = 'Vittore Branca'
        elif prettyNearPOI == 'Reset':
             prettyNearPOI = 'Circolo Reset'
        textAS = '\n\nAula studio più vicina: '+str(prettyNearPOI) + \
                    ', distanza: '+str(km)+' km'+ \
                    '. \nPer maggiori informazioni: /'+str(nearPOI)

        text = textMensa + textAS
        bot.sendMessage(chat_id=chat_id,text=text)

    def replytextCommand(self,bot,update,message,command,chat_id):
        textDB = pickledb.load('textcommandsDB.db', False)
        pyUniPd.writedb(update.message.to_dict())
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        reply = textDB.get(command)
        reply_markup = telegram.ReplyKeyboardHide()
        risp = bot.sendMessage(chat_id=chat_id, text=reply,
                               reply_markup=reply_markup)
        pyUniPd.writedb(risp.to_dict())

    def replykeyboardCommand(self,bot,update,message,command,chat_id):
        keyboardDB = pickledb.load('keyboardcommandsDB.db', False)
        pyUniPd.writedb(update.message.to_dict())
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        reply = keyboardDB.get(command)['text']
        markup = keyboardDB.get(command)['keyboard']
        reply_markup = telegram.ReplyKeyboardMarkup(markup)
        risp = bot.sendMessage(chat_id=chat_id, text=reply, 
                              reply_markup=reply_markup)
        pyUniPd.writedb(risp.to_dict())

    def replymensaCommand(self,bot,update,message,command,chat_id):
        pyUniPd.writedb(update.message.to_dict())
        mensaDB = pickledb.load('mensaDB.db', False)
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        reply = mensaDB.get(command)['text']
        lat = mensaDB.get(command)['coord']['lat']
        lon = mensaDB.get(command)['coord']['lon']
        reply_markup = telegram.ReplyKeyboardHide()
        risp = bot.sendMessage(chat_id=chat_id, 
               text=reply, reply_markup=reply_markup)
        pyUniPd.writedb(risp.to_dict())
        bot.sendLocation(chat_id=chat_id, latitude=lat, longitude=lon)

    def replyASCommand(self,bot,update,message,command,chat_id):
        pyUniPd.writedb(update.message.to_dict())
        mensaDB = pickledb.load('aulastudioDB.db', False)
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        reply = mensaDB.get(command)['text']
        lat = mensaDB.get(command)['coord']['lat']
        lon = mensaDB.get(command)['coord']['lon']
        reply_markup = telegram.ReplyKeyboardHide()
        risp = bot.sendMessage(chat_id=chat_id, 
               text=reply, reply_markup=reply_markup)
        pyUniPd.writedb(risp.to_dict())
        bot.sendLocation(chat_id=chat_id, latitude=lat, longitude=lon)