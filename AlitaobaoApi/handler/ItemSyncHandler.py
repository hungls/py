__author__ = 'hungls'

import tornado.ioloop
import tornado.web
import ast

from handler_helper_function import *

class ItemSyncHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("ItemSyncHandler")

    def post(self):
        data = self.get_argument('data', 'No data')
        # print data
        recs = ast.literal_eval(data)
        for rec in recs:
            for table,value in rec.iteritems():
                if table != "item":
                    for id_,item_ in value.iteritems():
                        query = self.build_insert_query(item_,table)
                        self.insert(query)
                if table == "item":
                    query_item = self.build_insert_query(value,"item")
                    self.insert(query_item)
            recs.remove(rec)
        self.write("Done")


    def insert(self,query):
        try:
            conn = get_connection_db()
            cur_ = conn.cursor()
            cur_.execute(query)
            conn.commit()
            return "True"
        except:
            return "False"
        finally:
            cur_.close()
            conn.close()


    def build_insert_query(self,item_,table):
        fns = u" "
        vls = u""
        vlu = ""
        fnu = u""

        for k,v in item_.iteritems():
            if v != None:
                if type(v) != unicode:
                    fns = fns + "`"+str(k)+"`"+","
                    vls = vls + "'" +str(v) + "'" + ","
                else:
                    fnu = fnu + "`"+str(k)+"`"+","
                    vlu = vlu + "'"+unicode(v)+"'"+","

        str_values = unicode(vls)+unicode(vlu)
        str_field = unicode(fns)+unicode(fnu)
        str_values = str_values[:-1]
        str_field = str_field[:-1]

        query = u"INSERT IGNORE INTO "+str(table)+" ("+unicode(str_field)+") VALUES ("+unicode(str_values)+")"
        return query