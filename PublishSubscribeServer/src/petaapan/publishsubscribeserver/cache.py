# -*- coding: utf-8 -*-
'''
Provides GAC database management support
Compatible with Python 2.5 or later

Created on 2010-09-10

@author: jonathan
'''


from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement

from google.appengine.api import memcache

class GacCache(object):

    def __init__(self):
        self.cache = memcache.Client()
        
    def load_cache(self, appkey, dbloader):
        self.ul = self.cache.get(appkey)
        if self.ul is None:
            self.ul = dbloader(appkey)
        return self.ul
    
    def update(self, appkey, instancekey, record):
        '''Update record in GAC cache and database storage'''
        record.put()
        self.ul[instancekey] = record
        self.cache.set(appkey, self.ul)