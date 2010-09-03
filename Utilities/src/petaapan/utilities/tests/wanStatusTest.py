# -*- coding: utf-8 -*-
'''
Created on 2010-08-29

@author: jonathan
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import unittest

import httplib
import string

import petaapan.utilities.wanStatus
from petaapan.utilities.wanStatusDef import *

TEST_PORT = 16160


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testWanStatus(self):
        url = 'http://localhost:8080/%s' % PRESENCE
        # Try to go online
        status = TEST_ONLINE
        ret = petaapan.utilities.wanStatus.send(status, TEST_PORT, url)
        self.assertEquals(ret[0] , httplib.ACCEPTED)
        self.assertTrue(string.find(ret[1], 'online') >= 0)

        # Try to go offline
        status = TEST_OFFLINE
        ret = petaapan.utilities.wanStatus.send(status, TEST_PORT, url)
        self.assertEquals(ret[0], httplib.ACCEPTED)
        self.assertTrue(string.find(ret[1], 'offline') >= 0)
        
        # Try to go online again
        status = TEST_ONLINE
        ret = petaapan.utilities.wanStatus.send(status, TEST_PORT, url)
        self.assertEquals(ret[0] , httplib.ACCEPTED)
        self.assertTrue(string.find(ret[1], 'online') >= 0)
        
        # Say we are coming online when we are already
        status = TEST_ONLINE
        ret = petaapan.utilities.wanStatus.send(status, TEST_PORT, url)
        self.assertEquals(ret[0] , httplib.ACCEPTED)
        self.assertTrue(string.find(ret[1], 'online') >= 0)

        # Now to go offline
        status = TEST_OFFLINE
        ret = petaapan.utilities.wanStatus.send(status, TEST_PORT, url)
        self.assertEquals(ret[0], httplib.ACCEPTED)
        self.assertTrue(string.find(ret[1], 'offline') >= 0)

        # And do it again
        status = TEST_OFFLINE
        ret = petaapan.utilities.wanStatus.send(status, TEST_PORT, url)
        self.assertEquals(ret[0], httplib.ACCEPTED)
        self.assertTrue(string.find(ret[1], 'offline') >= 0)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testWanStatus']
    unittest.main()