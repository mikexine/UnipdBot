#!/usr/bin/python
# -*- coding: utf-8 -*-

import telegram
from pyUniPd import pyUniPd
import ConfigParser
from time import sleep

config = ConfigParser.ConfigParser()
config.read('settings.ini')
token = config.get('main', 'token')
admin = str(config.get('main', 'admin'))
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
        usrChat = str(update.message.chat_id)

        if usrChat == admin:
            isAdmin = True
        else:
            isAdmin = False

        if '/stats' in message.lower():
            is_Stats = True
        else:
            is_Stats = False

        if isAdmin and is_Stats:
            uni.adminStats(bot, update, message, '/stats', chat_id)
            LAST_UPDATE_ID = update.update_id + 1
        elif is_Stats and not isAdmin:
            reply = "Non sei il mio creatore! Tradimento! Aiuto! Hahhahaha ciao :)"
            bot.sendMessage(chat_id=chat_id, text=reply)
            LAST_UPDATE_ID = update.update_id + 1
        else:
            pass

        commands = pyUniPd.commandlist('db/commandsDB.db')

        if pos is not None:
            uni.sendNearPOI(bot, chat_id, pos)
            LAST_UPDATE_ID = update.update_id + 1
        else:
            pass

        for c in range(len(commands)):
            if commands[c].lower() in message.lower():
                uni.reply(bot, update, message,
                          commands[c], chat_id)
                LAST_UPDATE_ID = update.update_id + 1

while True:
    if __name__ == "__main__":
        try:
            main()
        except:
            sleep(5)
