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
import SocketServer
import threading
import time

FROM_COLLABORATION = 'From Collaboration Server'

from petaapan.utilities import reportException
from petaapan.publishsubscribeserver.githubDef import GITHUB_ID
from petaapan.publishsubscribeserver.pssDef import GITHUB_NOTIFICATION


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def handle_one_request(self):
        self.server.log.debug('About to parse Github notification headers at %f'\
                              % time.clock())
        BaseHTTPServer.BaseHTTPRequestHandler.handle_one_request(self)
    
    def do_POST(self):
        self.server.log.debug('fromCollaboration received notification at %f'\
                              % time.clock())
        cl = int(self.headers.dict['content-length'])
        msg = json.loads(urllib.unquote_plus(self.rfile.read(cl)))
        try: # Send the HTTP response
            self.server.log.debug('fromCollaboration sending response at %f'\
                                  % time.clock())
            self.send_response(httplib.OK)
            self.send_header('content-length', '0')
            self.end_headers()
            self.wfile.write('\r\n')
        except Exception, ex:
            log = self.server.log.error if self.server.log else None
            log.debug('Acknowledge error in fromCollaboration %s' % str(ex))
            reportException.report(ex, log)
        # Pass the message up to those who know what to do with it
        if msg:
            if isinstance(msg, dict):
                payload = msg.get(GITHUB_ID)
                if payload and isinstance(payload, dict):
                    self.server.response.put((FROM_COLLABORATION, (GITHUB_NOTIFICATION, payload)),
                                             False)
                elif self.server.log:
                    self.server.log.error('Invalid Github  notification: %s'\
                                          % str(msg))

class HTTPReceptor(BaseHTTPServer.HTTPServer):
    def __init__(self, log=None, response_queue=None, host='0.0.0.0',
                 port=8080, handler_class=Handler):
        self._log = log
        self._response = response_queue
        SocketServer.TCPServer.__init__(self, (host, port), handler_class)
        
    @property
    def log(self):
        return self._log    
    
    @property
    def response(self):
        return self._response

class ServerManager(threading.Thread):
    
    def __init__(self, handler_class=Handler, host='0.0.0.0', port=8080,
                 response_queue=None, log=None):
        self._host = host
        self._port = port
        self._broken = False
        super(ServerManager, self).__init__(None, None,
                                            'From Collaboration HTTPServer')
        self._server = HTTPReceptor(log, response_queue, host, port,
                                    handler_class)
    
    def run(self): 
        try:
            self._server.serve_forever()
        except:
            self._broken = True       
        self._server = None
    
    @property
    def broken(self):
        return self._broken
    
    @property
    def server(self):
        return self._server
        