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
        pass
    

class ServerManager(object):
    def __init__(self, server_class=BaseHTTPServer.HTTPServer,
                 handler_class=Handler, host='localhost', port=8080):
        self._host = host
        self._port = port
        self._server = server_class((host, port), handler_class)
        self._shutdown = False