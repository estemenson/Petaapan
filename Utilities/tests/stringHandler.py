# -*- coding: utf-8 -*-
'''
A logging handler that simply writes to a StringIO object for testing usage

Created on 2010-08-28

@author: jonathan
'''
from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement

import StringIO
import logging

class StringHandler(logging.Handler):
    '''
    classdocs
    '''

    def __init__(self, level=logging.DEBUG):
#        super(StringHandler, self).__init__(level)
        logging.Handler.__init__(self, level)
        self.sink = StringIO.StringIO()
        
        
    def emit(self, record):
        self.sink.write(record)