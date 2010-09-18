# -*- coding: utf-8 -*-
'''

Provides a console logger for the standard Python logging system

Created on 2010-09-18

@author: jonathan
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


import sys

import logging
import atexit

class ConsoleLogger(object):


    def __init__(self, name, level=logging.ERROR):
        '''
        Constructor
        '''
        self._log = None
        self._enabled = False
        try:
            self._formatter = logging.Formatter(\
                     '%(name)s %(asctime)s %(levelname)-8s %(message)s')
            self._log = logging.getLogger(name)
            self._log.setLevel(level)
            self._log.propogate = False
            self.enable()
            def close_logging():
                if self._log and self._handler:
                    logging.shutdown([self._handler])
            atexit.register(close_logging)
        except Exception:
            pass
        
    def disable(self):
        if self._log and self._enabled:
            self._log.removeHandler(self._handler)
            self._handler.close()
            self._handler = None
            self._enabled = False
            
    def enable(self):
        if self._log and not self._enabled:
            self._handler = logging.StreamHandler(sys.stderr)
            self._handler.setFormatter(self._formatter)
            self._log.addHandler(self._handler)
            self._enabled = True
            
    def setLevel(self, level):
        if self._log:
            self._log.setLevel(level)
            
    def getLevel(self):
        if self._log:
            self._log.getEffectiveLevel()
            
    level = property(getLevel, setLevel)
        
        
        
        