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
import urlparse

from petaapan.publishsubscribeserver.pssDef import *
from petaapan.utilities.sendJsonMsg import send

SUBSCRIPTION_RESPONSE = 'Subscription Response'
SUBSCRIPTION_REQUEST = 'Subscription Request'
SUBSCRIPTION_SHUTDOWN = 'Subscription Shutdown'
TO_COLLABORATION = 'To Collaboration Server'

SHUTDOWN_TIMEOUT = 15


class ToCollaboration(threading.Thread):


    def __init__(self, response_queue,
                 host='0.0.0.0', port=8080, log=logging):
        self._command_queue = Queue.Queue()
        self._response_queue = response_queue
        self._host = host
        self._port = port
        self._log = log
        super(ToCollaboration, self).__init__(None, None,
                                              'To Collaboration HTTP Client')
        pass
    
    def constructSubscriptionMsg(self, state, publisher, url,
                                 port, userid, testing=False):
        msg = {REQ_SUBSCRIPTION: SUBSCRIBE if state else UNSUBSCRIBE,
               REQ_PUBLISHER: publisher, SUBSCRIBER_DNS: url,
               REQ_PORT: port, USER_ID: userid
              }
        if testing:
            msg[TESTING] = None
        return msg
    
    def subscribe(self, msg, url, dest_port=8080, log=None):
        self._command_queue.put((SUBSCRIPTION_REQUEST,
                                 (msg, url, dest_port, log)), False)
    
    def shutdown(self):
        self._command_queue.put((SUBSCRIPTION_SHUTDOWN, None), False)
        try:
            self._response_queue.get(True, SHUTDOWN_TIMEOUT)
        except Queue.Empty:
            pass
        
    def run(self):
        data = threading.local()
        data.do_shutdown = False
        
        # The internal command processing methods are nested here so
        # that they have access to the thread local data 
        
        def internalSubscription(self, args):
            msg, url, dest_port, log = args
            purl = urlparse.urlparse(url)
            host = purl[1]
            scheme = purl[0]
            if not scheme:
                url = 'http://' + url
                if not host:
                    purl = urlparse.urlparse(url)
                    host = purl[1]
            ret = send(msg, url, host, dest_port, log)
            self._response_queue.put((TO_COLLABORATION, (SUBSCRIPTION_RESPONSE,
                                                         (ret[0], ret[1], ret))),
                                      False)

        
        def internalShutdown(self, args=None): 
            data.do_shutdown = True
            self._response_queue.put(None, False)
        
              
        data.dispatcher = {SUBSCRIPTION_REQUEST: internalSubscription,
                           SUBSCRIPTION_SHUTDOWN: internalShutdown}
        
        while not data.do_shutdown:
            # Take a peek every 2 seconds to make
            # sure we are not shutting down
            try: 
                args = self._command_queue.get(True, 2)
                if args[0] in data.dispatcher:
                    data.dispatcher[args[0]](self, args[1])
            except Queue.Empty:
                pass
