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
import logging
import Queue

logging.basicConfig(level=logging.DEBUG)
logging.info('About to run test notification')

from publishsubscribeclient import fromCollaboration


class Test(unittest.TestCase):
    '''
    Tests that we can receive push notifications from Github
    You can run this test in two ways.
    1. Directly from Github. In this case you will need the following setup
       a) Start this test
       b) Tell Github to post the weblink to your workstation. You can do this
          using the Github administration facility for
          "ServiceHooks->Post-Receive URLs".
          You are responsible for setting up an environment that will allow the
          post (which comes over HTTP) to get to your workstation. You will
          need to provide Github with a URL that can reach your computer and
          then use the "Test Hook" button in "ServiceHooks->Post-Receive URLs"
          to send a notification message to you.
    
    2. Run via the Collaboration Server on Google App Engine 
       a) To run this test you must make sure that the Collaboration server is running
          on Google App Engine
       b) Tell Github to post the webhook to the collaboration server.
          You can do this using the Github administration facility for
          "ServiceHooks->Post-Receive URLs".
          You are responsible for setting up an environment that will allow the
          post (which comes over HTTP) to get to GAE. You will
          need to provide Github with a URL that can reach GAE.
       c) Start this test. 
       d) Use the "Test Hook" button in Github administration
          "ServiceHooks->Post-Receive URLs" to send a notification message to
          GAE which should then forward it to your computer.
    '''

    class HandleNotification(object):
        def __init__(self, test):
            self._test = test
            
        def __call__(self, msg):
            try:
                logging.info("Got payload from Google")
                self._test.assertTrue('payload' in msg)
                git = msg['payload']
                self._test.assertTrue('repository' in git)
                self._test.assertTrue('before' in git)
                self._test.assertTrue('commits' in git)
                self._test.assertTrue('after' in git)
                self._test.assertTrue('ref' in git)
                logging.info('Verified payload from Google is valid')
                
            finally:
                self._test.server.server.shutdown()
                pass

    def testName(self):
        response_queue = Queue.Queue()
        server = fromCollaboration.ServerManager(host='0.0.0.0', port=16160,
                                                 response_queue=response_queue,
                                                 log=logging)
        handler = self.HandleNotification(self)
        server.start()
        # WARNING: Will not return until a message has been received
        handler(response_queue.get(True))
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    import sys
    import os
    sys.path.insert(0, os.getcwd())
    
    unittest.main()