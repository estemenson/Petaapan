# -*- coding: utf-8 -*-
'''
Manages data from configuration file

Created on 2010-09-21

@author: jonathan
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import ConfigParser
import sys
from os.path import join, expanduser, expandvars

CONFIG_FILE = '.devenvcfg'
CONFIG_SYS_FILE = 'devenvcfg'

class Config(object):


    def __init__(self):
        self._cfg = ConfigParser.SafeConfigParser()
        # Read the configuration files
        self._cfg.read([join(expanduser('~'), CONFIG_FILE),
              expandvars(join('%ALLUSERSPROFILE%(%PROGRAMDATA%)',
                              CONFIG_FILE)
                 if sys.platform == 'win32'
                 else join('/etc', CONFIG_SYS_FILE))])
        
    @property
    def cfg(self):
        return self._cfg
        