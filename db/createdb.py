#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite

con = lite.connect('./logs.db')

with con:   
    cur = con.cursor()        
    cur.execute("DROP TABLE IF EXISTS log")
    cur.execute('''CREATE TABLE log (msg_id text, u_id text, username text, first_name text, last_name text, msg text, ch_id text, day text)''')