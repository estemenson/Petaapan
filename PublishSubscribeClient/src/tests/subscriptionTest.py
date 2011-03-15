# -*- coding: utf-8 -*-
'''
Created on 2011-02-20

@author: jonathan
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import httplib
import string
from publishsubscribeserver.pssDef import SUBACTION, SUBSCRIBE,\
            UNSUBSCRIBE,TEST_UNSUBSCRIBED, TEST_SUBSCRIBED, REQ_SUBSCRIPTION
from petaapan_utilities import sendJsonMsg


def subscriptionTest(testCase, server_name, server_port, status):
    url = 'http://%s:%s/%s' % (server_name, server_port, SUBACTION)
    ret = sendJsonMsg.send(status, url, dest_host=server_name,
                           dest_port=server_port)
    testCase.assertEquals(ret[0] , httplib.OK)
    testCase.assertTrue(string.find(ret[1], TEST_SUBSCRIBED) >= 0)

    # Try to unsubscribe
    status[REQ_SUBSCRIPTION] = UNSUBSCRIBE
    ret = sendJsonMsg.send(status, url, dest_host=server_name,
                           dest_port=server_port)
    testCase.assertEquals(ret[0], httplib.OK)
    testCase.assertTrue(string.find(ret[1], TEST_UNSUBSCRIBED) >= 0)
    
    # Try to subscribe again
    status[REQ_SUBSCRIPTION] = SUBSCRIBE
    ret = sendJsonMsg.send(status, url, dest_host=server_name,
                           dest_port=server_port)
    testCase.assertEquals(ret[0] , httplib.OK)
    testCase.assertTrue(string.find(ret[1], TEST_SUBSCRIBED) >= 0)
    
    # Say we are subscribing when we are already
    status[REQ_SUBSCRIPTION] = SUBSCRIBE
    ret = sendJsonMsg.send(status, url, dest_host=server_name,
                           dest_port=server_port)
    testCase.assertEquals(ret[0] , httplib.OK)
    testCase.assertTrue(string.find(ret[1], TEST_SUBSCRIBED) >= 0)

    # Now to go unsubscribe
    status[REQ_SUBSCRIPTION] = UNSUBSCRIBE
    ret = sendJsonMsg.send(status, url, dest_host=server_name,
                           dest_port=server_port)
    testCase.assertEquals(ret[0], httplib.OK)
    testCase.assertTrue(string.find(ret[1], TEST_UNSUBSCRIBED) >= 0)

    # And do it again
    status[REQ_SUBSCRIPTION] = UNSUBSCRIBE
    ret = sendJsonMsg.send(status, url, dest_host=server_name,
                           dest_port=server_port)
    testCase.assertEquals(ret[0], httplib.OK)
    testCase.assertTrue(string.find(ret[1], TEST_UNSUBSCRIBED) >= 0)
