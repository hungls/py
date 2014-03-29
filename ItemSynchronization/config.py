__author__ = 'hungls'

import ConfigParser

class Config:
    def __init__(self):
        self.config = ConfigParser.ConfigParser()

    def get_config(self):
        try:
            config = self.config
            config.readfp(open('config.ini'))
            return config
        except:
            print "Can't get config"

