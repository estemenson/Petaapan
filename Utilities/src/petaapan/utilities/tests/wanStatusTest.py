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
        url = 'http://localhost:8080/%s' % SUBACTION
        # Try to go online
        status = TEST_SUBSCRIBE
        ret = petaapan.utilities.wanStatus.send(status, TEST_PORT, url)
        self.assertEquals(ret[0] , httplib.ACCEPTED)
        self.assertTrue(string.find(ret[1], TEST_SUBSCRIBED) >= 0)

        # Try to go offline
        status = TEST_UNSUBSCRIBE
        ret = petaapan.utilities.wanStatus.send(status, TEST_PORT, url)
        self.assertEquals(ret[0], httplib.ACCEPTED)
        self.assertTrue(string.find(ret[1], TEST_UNSUBSCRIBED) >= 0)
        
        # Try to go online again
        status = TEST_SUBSCRIBE
        ret = petaapan.utilities.wanStatus.send(status, TEST_PORT, url)
        self.assertEquals(ret[0] , httplib.ACCEPTED)
        self.assertTrue(string.find(ret[1], TEST_SUBSCRIBED) >= 0)
        
        # Say we are coming online when we are already
        status = TEST_SUBSCRIBE
        ret = petaapan.utilities.wanStatus.send(status, TEST_PORT, url)
        self.assertEquals(ret[0] , httplib.ACCEPTED)
        self.assertTrue(string.find(ret[1], TEST_SUBSCRIBED) >= 0)

        # Now to go offline
        status = TEST_UNSUBSCRIBE
        ret = petaapan.utilities.wanStatus.send(status, TEST_PORT, url)
        self.assertEquals(ret[0], httplib.ACCEPTED)
        self.assertTrue(string.find(ret[1], TEST_UNSUBSCRIBED) >= 0)

        # And do it again
        status = TEST_UNSUBSCRIBE
        ret = petaapan.utilities.wanStatus.send(status, TEST_PORT, url)
        self.assertEquals(ret[0], httplib.ACCEPTED)
        self.assertTrue(string.find(ret[1], TEST_UNSUBSCRIBED) >= 0)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testWanStatus']
    unittest.main()