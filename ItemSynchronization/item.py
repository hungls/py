__author__ = 'hungls'

from db import *
import urllib
import urllib2


class Item:

    def __init__(self):
        self.connection = DB().get_connection()


    def get_items(self):
        try:
            connection = self.connection
            with connection:
                cur = connection.cursor()

                item_select = "SELECT * FROM item WHERE is_sync = 0"

                cur.execute(item_select)
                items = cur.fetchall()
                desc = cur.description

                result = []
                up_id = []
                for item in items:
                    record = {}

                    tmp = {}
                    for (index,column) in enumerate(item):
                        tmp[desc[index][0]] = column
                    record["item"] = tmp

                    item_id = item[0]
                    up_id.append(item_id)

                    attribute = self.get_table("item_attribute",item_id)
                    record["item_attribute"] = attribute

                    price_range = self.get_table("item_price_range",item_id)
                    record["item_price_range"] = price_range

                    property = self.get_table("item_property",item_id)
                    record["item_property"] = property

                    sku = self.get_table("item_sku",item_id)
                    record["item_sku"] = sku

                    category = self.get_table("item_category",item_id)
                    record["item_category"] = category

                    result.append(record)
                # print(result)
                self.set_id_update(up_id)
                self.do_sync(result)

        except:
            print "Error"
        finally:
            connection.close()


    def get_table(self,table,item_id):
        connection = self.connection
        with connection:
            cur_table = connection.cursor()
            item_table_select = "SELECT * FROM "+str(table)+" WHERE item_id = "+str(item_id)
            cur_table.execute(item_table_select)
            items = cur_table.fetchall()
            desc_table = cur_table.description

            attribute = {}
            for item in items:
                item_id = item[0]
                at = {}
                for (i,c) in enumerate(item):
                    at[desc_table[i][0]] = c
                attribute[item_id] = at
        return attribute


    def do_sync(self,data):
        mydata=[('data',data)]
        mydata=urllib.urlencode(mydata)
        path='http://localhost:9999/ItemSync/'
        req=urllib2.Request(path, mydata)
        req.add_header("Content-type", "application/x-www-form-urlencoded")
        page=urllib2.urlopen(req).read()
        if page == "Done":
            self.is_sync_update()


    def get_id_update(self):
        return self.update_id


    def set_id_update(self,up_id):
        self.update_id = up_id


    def is_sync_update(self):
        ids =  self.get_id_update()
        str_id = ""
        for id in ids:
            str_id = str(str_id)+str(id)+","
        in_id = str_id[:-1]
        sql_update = u"UPDATE item SET is_sync=1 WHERE item_id IN("+str(in_id)+")"
        try:
            connection = self.connection
            with connection:
                cur = connection.cursor()
                cur.execute(sql_update)
                connection.commit()
        except:
            print "Exept is_sync_update"
