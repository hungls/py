__author__ = 'hungls'

from config import *
import MySQLdb as mdb

class DB:
    def __init__(self):
        self.config = Config().get_config()

    def get_connection(self):
        try:
            db_host = self.config.get("mysql","mysql_host")
            db_user = self.config.get("mysql","mysql_user")
            db_pass = self.config.get("mysql","mysql_pass")
            db_name = self.config.get("mysql","mysql_database")

            con = mdb.connect(db_host, db_user, db_pass, db_name, charset="utf8", use_unicode=True)

            return con
        except:
            print "Create connection mysql error"

