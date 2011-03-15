# -*- coding: utf-8 -*-
'''
Created on 2010-08-28

@author: jonathan
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement

import unittest
import logging
import string
import petaapan.utilities.reportException
import petaapan.utilities.tests.stringHandler


class TestError(Exception):
    def __init__(self, args):
        self.args = args
        
class TestReportError(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger('TestReportErrorLogger')
        self.logger.setLevel(logging.DEBUG)
        self.handler = petaapan.utilities.tests.stringHandler.StringHandler()
        self.logger.addHandler(self.handler)
        

    def testReportError(self):
        error_code = 100
        error_description = 'This is an error description'
        supplemental_arg1 = 'Supplemental argument 1'
        supplemental_arg2 = 'Supplemental argument 2'
        try:
            raise TestError((error_code, error_description,
                             supplemental_arg1, supplemental_arg2 ))
        except TestError , ex:
            st = petaapan.utilities.reportException.report(ex, self.logger)
            found = 0
            
            # Make sure all the exception data is present
            it1 = (str(error_code), error_description,
                   supplemental_arg1,supplemental_arg2).__iter__()
            val = it1.next()
            for line in st:
                try:
                    if found == 4: break
                    if line[:1] == '\t':
                        ix = string.find(line, val)
                        self.assertTrue(ix > 0)
                        found += 1
                        val = it1.next()
                except StopIteration:
                    break
            self.assertTrue(found == 4)
            
            # Make sure everything got logged
            loglines = self.handler.sink
            it2 = st.__iter__()
            for line in loglines:
                ln = it2.next()
                self.assertTrue(string.find(line.getMessage(), ln) >= 0)
            
                

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testReportError']
    unittest.main()