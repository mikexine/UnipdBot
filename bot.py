#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ParseMode, Bot
import logging
import pyUnipdbot
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('settings.ini')
token = str(config.get('main', 'token'))
servicetoken = str(config.get('main', 'servicetoken'))

TOPCOMMANDS = ['start', 'home', 'help', 'botinfo',
               'mensa', 'aulastudio', 'biblioteca',
               'udupadova', 'diritto_studio']

commands = pyUnipdbot.commandList()

# logging
if str(config.get('main', 'logging')) == "INFO":
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
else:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)

logger = logging.getLogger(__name__)


def home(bot, update):
    pyUnipdbot.writedb(update.message.to_dict())
    reply, markup = pyUnipdbot.home()
    bot.sendMessage(update.message.chat_id,
                    text=reply,
                    reply_markup=ReplyKeyboardMarkup(markup))


def botinfo(bot, update):
    pyUnipdbot.writedb(update.message.to_dict())
    reply, markup = pyUnipdbot.botInfo()
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=reply,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=ReplyKeyboardMarkup(markup))


def mensa(bot, update):
    pyUnipdbot.writedb(update.message.to_dict())
    reply, markup = pyUnipdbot.mensa()
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=reply,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=ReplyKeyboardMarkup(markup))


def aulastudio(bot, update):
    pyUnipdbot.writedb(update.message.to_dict())
    reply, markup = pyUnipdbot.aulastudio()
    bot.sendMessage(update.message.chat_id,
                    text=reply,
                    reply_markup=ReplyKeyboardMarkup(markup))


def biblioteca(bot, update):
    pyUnipdbot.writedb(update.message.to_dict())
    reply, markup = pyUnipdbot.biblioteca()
    bot.sendMessage(update.message.chat_id,
                    text=reply,
                    reply_markup=ReplyKeyboardMarkup(markup))


def dirittostudio(bot, update):
    pyUnipdbot.writedb(update.message.to_dict())
    reply, markup = pyUnipdbot.dirittostudio()
    bot.sendMessage(update.message.chat_id,
                    text=reply,
                    reply_markup=ReplyKeyboardMarkup(markup))


def udupadova(bot, update):
    pyUnipdbot.writedb(update.message.to_dict())
    reply, markup = pyUnipdbot.udupadova()
    bot.sendMessage(update.message.chat_id,
                    text=reply,
                    reply_markup=ReplyKeyboardMarkup(markup))


def replier(bot, update):
    pyUnipdbot.writedb(update.message.to_dict())
    command = str(update.message.text).replace('/', '')
    command.lower()
    reply, markup, lat, lon = pyUnipdbot.replier(command)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=reply,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=ReplyKeyboardMarkup(markup))
    if lat is not None and lon is not None:
        bot.sendLocation(update.message.chat_id,
                         latitude=lat,
                         longitude=lon)


def position(bot, update):
    print "running position"
    msg = update.message.to_dict()
    pyUnipdbot.writedb(msg)
    try:
        usrCoord = msg['location']
        reply, markup = pyUnipdbot.position(usrCoord)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=reply,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=ReplyKeyboardMarkup(markup))
    except:
        pass


def simpleText(bot, update):
    print "running simpletext"
    msg = update.message.to_dict()
    pyUnipdbot.writedb(msg)
    text = ""
    try:
        text += str(msg['from']['id'])
        bot.sendMessage(chat_id=27002116,
                        text=text)
    except:
        pass
    bot.forwardMessage(chat_id=27002116,
                       from_chat_id=update.message.chat_id,
                       message_id=update.message.message_id)


def admin_reply(bot, update, args):
    msg = update.message.to_dict()
    pyUnipdbot.writedb(msg)
    servicer = Bot(token=servicetoken)
    if update.message.from_user.id == 27002116:
        try:
            tmp = "/reply " + args[0] + " "
            sent = bot.sendMessage(chat_id=args[0],
                                   text=str(update.message.text).replace(tmp, ""))
            servicer.sendMessage(chat_id=27002116, text=str(sent))
        except:
            servicer.sendMessage(chat_id=27002116, text="error happened") 
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="error - you're not powerful enough")



def error(bot, update, error):
    try:
        ch_id = "27002116"
        starter = Bot(token=token)
        txt = "An error happened"
        starter.sendMessage(ch_id, text=txt)
    except:
        pass
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addHandler(CommandHandler("help", home))
    dp.addHandler(CommandHandler("start", home))
    dp.addHandler(CommandHandler("home", home))

    dp.addHandler(CommandHandler("botinfo", botinfo))

    dp.addHandler(CommandHandler("mensa", mensa))
    dp.addHandler(CommandHandler("aulastudio", aulastudio))
    dp.addHandler(CommandHandler("biblioteca", biblioteca))
    dp.addHandler(CommandHandler("udupadova", udupadova))
    dp.addHandler(CommandHandler("diritto_studio", dirittostudio))

    for command in commands:
        dp.addHandler(CommandHandler(command, replier))

    dp.addHandler(CommandHandler("reply", admin_reply, pass_args=True))

    dp.addHandler(MessageHandler([Filters.location], position))
    dp.addHandler(MessageHandler([Filters.text], simpleText))
    dp.addHandler(MessageHandler([Filters.audio], simpleText))
    dp.addHandler(MessageHandler([Filters.photo], simpleText))
    dp.addHandler(MessageHandler([Filters.document], simpleText))
    dp.addHandler(MessageHandler([Filters.sticker], simpleText))
    dp.addHandler(MessageHandler([Filters.video], simpleText))
    dp.addHandler(MessageHandler([Filters.voice], simpleText))
    dp.addHandler(MessageHandler([Filters.contact], simpleText))

    dp.addErrorHandler(error)
    updater.start_polling()

    ch_id = "27002116"
    starter = Bot(token=token)

    txt = "I'm starting"
    starter.sendMessage(ch_id, text=txt)

    updater.idle()

    txt = "Bot stopped!"
    starter.sendMessage(ch_id, text=txt)

if __name__ == '__main__':
    main()
