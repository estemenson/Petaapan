# -*- coding: utf-8 -*-
'''
Created on 2010-10-07

@author: jonathan
'''


from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import threading
import logging
import Queue

from petaapan.publishsubscribeserver.pssDef import *

SUBSCRIPTION_RESPONSE = 'Subscription Response'
SUBSCRIPTION_REQUEST = 'Subscription Request'
SUBSCRIPTION_SHUTDOWN = 'Subscription Shutdown'
TO_COLLABORATION = 'To Collaboration Server'


class ToCollaboration(threading.Thread):


    def __init__(self, response_queue,
                 host='0.0.0.0', port=8080, log=logging):
        self._command_queue = Queue.Queue()
        self._response_queue = response_queue,
        self._host = host
        self._port = port
        self._log = log
        super(ToCollaboration, self).__init__()
        pass
    
    def constructSubscriptionMsg(self, state, publisher, url,
                                 port, userid, testing=False):
        msg = {REQ_SUBSCRIPTION: SUBSCRIBE if state else UNSUBSCRIBE,
               REQ_PUBLISHER: publisher, SUBSCRIBER_DNS: url,
               REQ_PORT: port, USER_ID: userid
              }
        if testing:
            msg[TESTING]
        return msg
    
    def subscribe(self, msg, url):
        pass
    
    def shutdown(self):
        pass
        
    def run(self):
        data = threading.local()
        data.do_shutdown = False
        
        # The internal command processing methods are nested here so
        # that they have access to the thread local data 
        
        def internalSubscription(self, args):
            pass
        
        def internalShutdown(self): 
            pass
        
              
        data.dispatcher = {SUBSCRIPTION_REQUEST: internalSubscription,
                           SUBSCRIPTION_SHUTDOWN: internalShutdown}
        while not data.do_shutdown:
            # Take a peek every 2 seconds to make
            # sure we are not shutting down
            try: 
                args = self._internalQueue.get(True, 2)
                if args[0] in data.dispatcher:
                    data.dispatcher[args[0]](self, args[1])
            except Queue.Empty:
                pass
