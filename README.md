# UnipdBot

An unofficial Telegram bot for students of [University of Padua](http://www.unipd.it/) (Unipd) - try it at [@UnipdBot](https://telegram.me/UnipdBot)!

Still in early stage, the code is messy and the bot might be unresponsive. Be careful!


### Description

Simple Telegram bot! Data source: http://unidata.xyz. 
Backend's source code: https://github.com/mikexine/unidata-backend


### Running the bot

Just some simple instructions if you want to test the bot

- `pip install -r requirements.txt`
- Rename settings.ini.sample to settings.ini
- Create an access token with Telegram's @Botfather and place it in `settings.ini`. 
- Switch into the `db` folder and run `python createdb_logs.py`.
- Run `mydb.py` to create a local `pickledb` database in which you'll store commands. 
- If you want to use the `/stats` command, you must retrieve your Telegram User Id and put it into `settings.ini`.
- The `auth` setting in `settings.ini` is needed in `update_mensa.py`. Only when a valid `auth` token is supplied, you'll be able to make `PUT/POST/DELETE` requests to unipd.xyz. `GET` requests are all public.


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
