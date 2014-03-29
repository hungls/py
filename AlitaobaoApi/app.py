__author__ = 'hungls'


import tornado.ioloop
import tornado.web

from handler_helper_function import *

application = tornado.web.Application([
    (r"/", get_handler("MainHandler")),
    (r"/ItemSync/",get_handler("ItemSyncHandler"))
])

if __name__ == "__main__":
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()