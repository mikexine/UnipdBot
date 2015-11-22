# UnipdBot
An unofficial Telegram bot for students of [University of Padua](http://www.unipd.it/) (Unipd) - try it at [@UnipdBot](https://telegram.me/UnipdBot)!

Still in early stage, the code is messy and the bot might be unresponsive. Be careful!


### Description
I wanted to make a bot with commands that can be upgraded and changed at any time, without having to mess with the code. 

The bot pulls commands from a [Deployd app](http://deployd.com/) running at [unipd.xyz](http://unipd.xyz)... but this part has to be improved more. An example: http://unipd.xyz/commands

Moreover, the bot can send data parsed from the University's website. An example is in the [`update_mensa.py`](https://github.com/mikexine/UnipdBot/blob/master/update_mensa.py) file: this one updates the Bot's APIs with data about the Unipd's canteens (today's menu and open or close). More data and commands will be added soon.


### Running the bot

Just some simple instructions if you want to test the bot

- `pip install -r requirements.txt`
- Rename settings.ini.sample to settings.ini
- Create an access token with Telegram's @Botfather and place it in `settings.ini`. 
- Switch into the `db` folder and run `python createdb_logs.py`.
- Run `mydb.py` to create a local `pickledb` database in which you'll store commands. 
- If you want to use the `/stats` command, you must retrieve your Telegram User Id and put it into `settings.ini`.
- The `auth` setting in `settings.ini` is needed in `update_mensa.py`. Only when a valid `auth` token is supplied, you'll be able to make `PUT/POST/DELETE` requests to unipd.xyz. `GET` requests are all public.


### Using the Unipd's [Unofficial APIs](http://unipd.xyz).

Feel free to use the data provided by the Unipd's [Unofficial APIs](http://unipd.xyz)! Only `GET` requests are available. 

Endpoints:

- http://unipd.xyz/aulastudio: data about Unipd's study rooms.
- http://unipd.xyz/mensa: data about Unipd's canteens.
- http://unipd.xyz/biblioteca: data about Unipd's libraries.


### License and credits

Read [LICENSE](https://github.com/mikexine/UnipdBot/blob/master/LICENSE) file for @UnipdBot's license.

This bot uses also:

- [python-telegram-bot](https://github.com/leandrotoledo/python-telegram-bot)
- [beautifulsoup4](http://www.crummy.com/software/BeautifulSoup/)
- [requests](http://docs.python-requests.org/en/latest/)
- [pickledb](https://pythonhosted.org/pickleDB/)
- [geopy](https://github.com/geopy/geopy)
- [simplejson](https://pypi.python.org/pypi/simplejson/)
- [arrow](http://crsmithdev.com/arrow/)
- Python, Internet, Telegram, and all those nice things.

### Contact

For anything (bugs, contributing, saying hi!), contact me on Telegram at [@mikexine](https://telegram.me/mikexine) or via e-mail at [mikexine@gmail.com](mailto:mikexine@gmail.com)
