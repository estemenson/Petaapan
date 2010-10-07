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

FROM_COLLABORATION = 'From Collaboration Server'

from petaapan.utilities import reportException

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def do_POST(self):
        msg = json.loads(urllib.unquote_plus(self.rfile.read()))
        try: # Send the HTTP response
            self.send_response(httplib.OK)
        except Exception, ex:
            reportException(ex, self.server.log.error
                                if self.server.log != None else None)
        # Pass the message up to those who know what to do with it
        if self.server.response is not None:
            self.server.response.put((FROM_COLLABORATION, msg), False)
    

class ServerManager(threading.Thread):
    
    def __init__(self, server_class=BaseHTTPServer.HTTPServer,
                 handler_class=Handler, host='localhost', port=8080,
                 response_queue=None, log=None):
        self._host = host
        self._port = port
        self._log = log
        self._broken = False
        self._response = response_queue
        super(ServerManager, self).__init__(None, None, 'HTTPServer')
        self._server = server_class((host, port), handler_class)
    
    def run(self): 
        try:
            self._server.serve_forever()
        except:
            self._broken = True       
        self._server = None
        self._log = None
        self._response = None
        
    @property
    def log(self):
        return self._log
    
    @property
    def response(self):
        return self._response
    
    @property
    def broken(self):
        return self._broken
    
    @property
    def server(self):
        return self._server
        