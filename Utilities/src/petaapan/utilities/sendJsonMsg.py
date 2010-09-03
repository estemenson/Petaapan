# -*- coding: utf-8 -*-
'''
Send online/offline status notification to AgileServers
Compatible with Python 2.5 or later

Created on 2010-08-29

@author: jonathan
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json
import httplib

def send(msg, url, dest_host='localhost', dest_port=8080):
    try:
        conn = httplib.HTTPConnection(dest_host, dest_port)
        if conn is not None:
            conn.connect()
            conn.request('POST', url, json.dumps(msg))
            ret = conn.getresponse()
            return (ret.status, ret.reason)
    finally:
        if conn is not None: conn.close()
        