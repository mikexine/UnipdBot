#!/usr/bin/python
# -*- coding: utf-8 -*-
import telegram
import datetime
from pyUniPd import pyUniPd
import ConfigParser

config  = ConfigParser.ConfigParser()
config.read('settings.ini')
token = config.get('main','token')

LAST_UPDATE_ID = None
uni = pyUniPd()


def main():
    global LAST_UPDATE_ID
    bot = telegram.Bot(token)
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None
    while True:
        unipd(bot)


def unipd(bot):
    global LAST_UPDATE_ID
    for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
        chat_id = update.message.chat_id
        message = update.message.text.encode("utf-8")
        pos = update.message.location

        textcommands = pyUniPd.commandlist('textcommandsDB.db')
        keyboardcommands = pyUniPd.commandlist('keyboardcommandsDB.db')
        mensacommands = pyUniPd.commandlist('mensaDB.db')

        if pos != None:
            uni.sendNearPOI(bot,chat_id,pos)
            LAST_UPDATE_ID = update.update_id + 1          
        else:
            pass

        for textcommand in range(len(textcommands)):
            if textcommands[textcommand].lower() in message.lower():
                uni.replytextCommand(bot,update,message,textcommands[textcommand],chat_id)
                LAST_UPDATE_ID = update.update_id + 1

        for keyboardcommand in range(len(keyboardcommands)):
            if keyboardcommands[keyboardcommand].lower() in message.lower():
                uni.replykeyboardCommand(bot,update,message,keyboardcommands[keyboardcommand],chat_id)
                LAST_UPDATE_ID = update.update_id + 1

        for mensacommand in range(len(mensacommands)):
            if mensacommands[mensacommand].lower() in message.lower():
                uni.replymensaCommand(bot,update,message,mensacommands[mensacommand],chat_id)
                LAST_UPDATE_ID = update.update_id + 1




while True:
    if __name__ == "__main__":
        main()

