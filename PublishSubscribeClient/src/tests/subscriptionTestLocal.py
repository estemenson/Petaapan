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

from  publishsubscribeserver.pssDef import SUBSCRIBE,REQ_SUBSCRIPTION,\
    REQ_PORT,REQ_PUBLISHER, USER_ID, SUBSCRIBER_DNS
from publishsubscribeserver.githubDef import GITHUB
from tests.subscriptionTest import subscriptionTest

# Name of Github repository we are using for testing
GITHUB_REPOSITORY = '/jfgossage/Storyapp'
# DNS name of subscription server
SUB_NAME = 'localhost'
# Port we will send publish/subscribe requests to
SUB_PORT = 8080
# Name of user connecting to publish/subscribe server
SUBSCRIBER_NAME = 'jgossage@gmail.com'
# Name of connection where subscriber will receive collaboration notices
COLLABORATION_NAME = 'localhost'
# Port where subscriber will receive collaboration notices
COLLABORATION_PORT = 16160


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testSubscriptionLocal(self):
        # Try to subscribe
        status = {REQ_SUBSCRIPTION: SUBSCRIBE,
                  REQ_PUBLISHER: GITHUB + GITHUB_REPOSITORY,
                  USER_ID: SUBSCRIBER_NAME,
                  REQ_PORT: COLLABORATION_PORT,
                  SUBSCRIBER_DNS: COLLABORATION_NAME}
        subscriptionTest(self, SUB_NAME, SUB_PORT, status)          
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSubscription']
    unittest.main()