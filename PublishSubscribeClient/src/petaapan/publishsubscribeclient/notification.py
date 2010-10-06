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
import threading

NOTIFICATION = 'Google Notification'

from petaapan.utilities import reportException

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def do_POST(self):
        msg = json.loads(urllib.unquote_plus(self.rfile.read()))
        try: # Send the HTTP response
            self.send_response(httplib.OK)
        except Exception, ex:
            reportException(ex, ServerManager.Log.error
                                if ServerManager.Log != None else None)
        # Pass the message up to those who know what to do with it
        if ServerManager.Response is not None:
            ServerManager.Response.put((NOTIFICATION, msg), False)
    

class ServerManager(threading.Thread):
    Log = None
    Response = None
    
    def __init__(self, server_class=BaseHTTPServer.HTTPServer,
                 handler_class=Handler, host='localhost', port=8080,
                 response_queue=None, log=None):
        self._host = host
        self._port = port
        ServerManager.Log = log
        ServerManager.Response = response_queue
        super(ServerManager, self).__init__(None, None, 'HTTPServer')
        self._server = server_class((host, port), handler_class)
        self._shutdown = False
    
    def run(self): 
        while not self._shutdown:
            self._server.handle_request()       
        self._server = None
        ServerManager.Log = None
        ServerManager.Response = None

    def getShutdown(self):
        return self._shutdown
    def setShutdown(self, value):
        self._shutdown = value
    shutdown = property(getShutdown, setShutdown)
        