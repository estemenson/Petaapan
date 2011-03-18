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
        self._log = None
        self._enabled = False
        self._handler = None
        try:
            self._formatter = logging.Formatter(\
                     '%(name)s %(asctime)s %(levelname)-8s %(message)s')
            self._log = logging.getLogger(name)
            self._log.setLevel(level)
            self._log.propogate = False
            self._handler = logging.StreamHandler()
            self._handler.setLevel(level)
            self._handler.setFormatter(self._formatter)
            self._log.addHandler(self._handler)
            self.enable()
            def close_logging():
                if self._log and self._handler:
                    logging.shutdown()
#                    logging.shutdown([self._handler])
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
    def debug(self, msg):
        if self._log and self._enabled:
            self._log.debug(msg)
    def error(self, msg):
        if self._log and self._enabled:
            self._log.error(msg)
    def critical(self, msg):
        if self._log and self._enabled:
            self._log.critical(msg)
    def warning(self, msg):
        if self._log and self._enabled:
            self._log.warning(msg)
    def info(self, msg):
        if self._log and self._enabled:
            self._log.info(msg)
    def exception(self, msg):
        if (self._log and self._enabled):
            self._log.exception(msg)
        
    def setLevel(self, level):
        if self._log:
            if level == 'error':
                _level = logging.ERROR
            elif level == 'critical':
                _level = logging.CRITICAL
            elif level == 'warning':
                _level = logging.WARNING
            elif level == 'debug':
                _level = logging.DEBUG
            elif level == 'info':
                _level = logging.INFO
            else:
                _level = level
            self._log.setLevel(_level)
            
    def getLevel(self):
        if self._log:
            self._log.getEffectiveLevel()
            
    level = property(getLevel, setLevel)
    
    @property
    def logger(self):
        return self._log
        
        
        
        