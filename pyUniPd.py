#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import telegram
import sqlite3
import time
import pickledb



# db = pickledb.load('aulastudiocommandsDB.db',False)
# aulastudiocommands = u.commandlist(db)


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
            h = datetime.datetime.fromtimestamp(int(mdict["date"])).strftime("%Y-%m-%d %H:%M:%S")
        except:
            pass

        with con: 
            cur = con.cursor()
            cur.execute("INSERT INTO log VALUES (?,?,?,?,?,?,?,?)", (a, b, c, d, e, f, g, h))

    def replytextCommand(self,bot,update,message,command,chat_id):
        textDB = pickledb.load('textcommandsDB.db', False)
        pyUniPd.writedb(update.message.to_dict())
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        reply = textDB.get(command)
        risp = bot.sendMessage(chat_id=chat_id, text=reply)
        pyUniPd.writedb(risp.to_dict())

    def replykeyboardCommand(self,bot,update,message,command,chat_id):
        keyboardDB = pickledb.load('keyboardcommandsDB.db', False)
        pyUniPd.writedb(update.message.to_dict())
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        reply = keyboardDB.get(command)['text']
        markup = keyboardDB.get(command)['keyboard']
        reply_markup = telegram.ReplyKeyboardMarkup(markup)
        risp = bot.sendMessage(chat_id=chat_id, text=reply, reply_markup=reply_markup)
        pyUniPd.writedb(risp.to_dict())

    def replymensaCommand(self,bot,update,message,command,chat_id):
        mensaDB = pickledb.load('mensaDB.db', False)
        pyUniPd.writedb(update.message.to_dict())
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        reply = mensaDB.get(command)['text']
        lat = mensaDB.get(command)['coord']['lat']
        lon = mensaDB.get(command)['coord']['lon']
        reply_markup = telegram.ReplyKeyboardHide()

        risp = bot.sendMessage(chat_id=chat_id, text=reply, reply_markup=reply_markup)
        pyUniPd.writedb(risp.to_dict())
        bot.sendLocation(chat_id=chat_id, latitude=lat, longitude=lon)


    def help(self):
        return help

    def allmensa(self):
        return mensa

    def mensa(self, mensa):
        txt = "La mensa %s è in %s\nOrari: %s\nTelefono: %s" % (mense[mensa]["Nome"],mense[mensa]["Ind"], mense[mensa]["orari"], mense[mensa]["tel"])
        lat = mense[mensa]["coord"]["lat"]
        lon = mense[mensa]["coord"]["lon"]
        return txt, lat, lon




