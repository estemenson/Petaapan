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
import urllib
import BaseHTTPServer
import logging

from petaapan.utilities import reportException

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        msg = json.loads(urllib.unquote_plus(self.rfile.read()))
        try:
            self.send_response(httplib.OK)
        except Exception, ex:
            reportException(ex, logging.error)
        for o in ServerManager._observers:
            o(msg)
    

class ServerManager(object):
    _observers = []
    
    def __init__(self, server_class=BaseHTTPServer.HTTPServer,
                 handler_class=Handler, host='localhost', port=8080):
        self._host = host
        self._port = port
        self._server = server_class((host, port), handler_class)
        self._shutdown = False
    
    def run(self): 
        while not self._shutdown:
            self._server.handle_request()       
        ServerManager._observers = None
        self._server = None
        
    def addObserver(self, observer):
        ServerManager._observers.append(observer)
    def removeObserver(self, observer):
        ServerManager._observers.remove(observer)

    def getShutdown(self):
        return self._shutdown
    def setShutdown(self, value):
        self._shutdown = value
    shutdown = property(getShutdown, setShutdown)
        