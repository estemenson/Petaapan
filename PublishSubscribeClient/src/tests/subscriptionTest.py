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

from pssDef import *
from githubDef import *
from petaapan.utilities import sendJsonMsg

TEST_PORT = 16160


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testSubscription(self):
        url = 'http://poseidon:8080/%s' % SUBACTION
        # Try to subscribe
        status = {REQ_SUBSCRIPTION: TEST_SUBSCRIBE,
                  REQ_PUBLISHER: GITHUB + '/jfgossage/Storyapp',
                  REQ_PORT: TEST_PORT}
                  
        ret = sendJsonMsg.send(status, url)
        self.assertEquals(ret[0] , httplib.OK)
        self.assertTrue(string.find(ret[1], TEST_SUBSCRIBED) >= 0)

        # Try to unsubscribe
        status[REQ_SUBSCRIPTION] = TEST_UNSUBSCRIBE
        ret = sendJsonMsg.send(status, url)
        self.assertEquals(ret[0], httplib.OK)
        self.assertTrue(string.find(ret[1], TEST_UNSUBSCRIBED) >= 0)
        
        # Try to subscribe again
        status[REQ_SUBSCRIPTION] = TEST_SUBSCRIBE
        ret = sendJsonMsg.send(status, url)
        self.assertEquals(ret[0] , httplib.OK)
        self.assertTrue(string.find(ret[1], TEST_SUBSCRIBED) >= 0)
        
        # Say we are subscribing when we are already
        status[REQ_SUBSCRIPTION] = TEST_SUBSCRIBE
        ret = sendJsonMsg.send(status, url)
        self.assertEquals(ret[0] , httplib.OK)
        self.assertTrue(string.find(ret[1], TEST_SUBSCRIBED) >= 0)

        # Now to go unsubscribe
        status[REQ_SUBSCRIPTION] = TEST_UNSUBSCRIBE
        ret = sendJsonMsg.send(status, url)
        self.assertEquals(ret[0], httplib.OK)
        self.assertTrue(string.find(ret[1], TEST_UNSUBSCRIBED) >= 0)

        # And do it again
        status[REQ_SUBSCRIPTION] = TEST_UNSUBSCRIBE
        ret = sendJsonMsg.send(status, url)
        self.assertEquals(ret[0], httplib.OK)
        self.assertTrue(string.find(ret[1], TEST_UNSUBSCRIBED) >= 0)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSubscription']
    unittest.main()