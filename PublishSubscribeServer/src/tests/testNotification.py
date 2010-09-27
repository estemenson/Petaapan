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

logging.basicConfig(level=logging.DEBUG)
logging.info('About to run test notification')

if __name__ != "__main__":
    import notification


class Test(unittest.TestCase):

    class HandleNotification(object):
        def __init__(self, test, context):
            self._test = test
            self._context = context
            
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
#                self._context.shutdown = True
                pass

    def testName(self):
        server = notification.ServerManager(host='0.0.0.0', port=16160)
        server.addObserver(Test.HandleNotification(self, server))
        server.run()
        # WARNING: Will not return until a message has been received
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    import sys
    import os
    sys.path.insert(0, os.getcwd())
    import notification
    
    unittest.main()