__author__ = 'hungls'

import ConfigParser
import json
import importlib
import datetime
import MySQLdb as mdb

config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))


def get_current_day_timestamp():
    t=datetime.date.today()
    now = datetime.datetime(t.year, t.month, t.day) - datetime.timedelta(hours=7)
    return int((now - datetime.datetime.utcfromtimestamp(0)).total_seconds())

def get_current_timestamp():
    import time
    t = time.time()
    return int(t)

def get_handler(handler_name):
    m = importlib.import_module('handler.'+handler_name)
    try:
        c = getattr(m, handler_name)
        return c
    except:
        print "ERROR: khong tim thay class `"+handler_name + "`"

def get_connection_db():
    try:
        db_host = config.get("mysql","mysql_host")
        db_user = config.get("mysql","mysql_user")
        db_pass = config.get("mysql","mysql_pass")
        db_name = config.get("mysql","mysql_database")

        con = mdb.connect(db_host, db_user, db_pass, db_name, charset="utf8", use_unicode=True)

        return con
    except:
        print "Create connection mysql error"
