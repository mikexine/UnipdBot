# UnipdBot
An unofficial Telegram bot for students of http://www.unipd.it/ - try it at https://telegram.me/UnipdBot

If you want to help, contact me!

Still in early stage, the code is messy and the bot might be unresponsive. Be careful!

If you want to help, contact me on Telegram at [@mikexine](https://telegram.me/mikexine)


I wanted to make a bot with commands that can be upgraded and changed at any time, without having to mess with the code. 

The bot pulls commands from a [Deployd app](http://deployd.com/) running at [unipd.xyz](http://unipd.xyz)... but this part has to be improved a LOT. An example: http://unipd.xyz/mensa

Moreover, the bot sends data parsed from the University's website. An example is in the `[update_mensa.py](https://github.com/mikexine/UnipdBot/blob/master/update_mensa.py)` file: this one updates the bot with data about the University's canteens (today's menu and open or close). More data and commands will be added soon.

To run it, create an access token with Telegram's @Botfather, place it in `settings.ini.sample` and rename it to `settings.ini`. Then, switch into the `db` folder and run `python createdb_logs.py`: it will create a sqlite3 db in which will be stored every message (with a command) sent to the bot and every bot's reply.