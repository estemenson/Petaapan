# -*- coding: utf-8 -*-
'''
Created on 2010-09-23

@author: jonathan
'''


from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import unittest
import notification


class Test(unittest.TestCase):


    def testName(self):
        notification.ServerManager()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()