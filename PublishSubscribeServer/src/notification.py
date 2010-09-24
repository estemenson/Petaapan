# -*- coding: utf-8 -*-
'''
Notification receiver
Receives notification from github describing the changes that took place in
the last push to Github. Notification received in the same format as it was
sent from Github
Invoked from subscriber application on subscriber's workstation

Created on 2010-09-14

@author: jonathan
'''


from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json
import httplib
import BaseHTTPServer

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        msg = json.load(self.rfile)
        self.send_response(httplib.OK)
        for o in self._observers:
            o.notify(msg)
    

class ServerManager(object):
    def __init__(self, server_class=BaseHTTPServer.HTTPServer,
                 handler_class=Handler, host='localhost', port=8080):
        self._host = host
        self._port = port
        self._server = server_class((host, port), handler_class)
        self._shutdown = False
        self._observers = []
    
    def run(self): 
        while not self._shutdown:
            self._server.handle_request()       
        for o in self._observers:
            self._observers.remove(o)
        self._observers = None
        self._server = None
        
    def addObserver(self, observer):
        self._observer.append(observer)
    def removeObserver(self, observer):
        self._observers.remove(observer)

    def getShutdown(self):
        return self._shutdown
    def setShutdown(self, value):
        self._shutdown = value
    shutdown = property(getShutdown, setShutdown)
        