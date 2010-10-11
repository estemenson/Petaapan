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
import urllib
import logging
from petaapan.utilities import reportException

def send(msg, url, dest_host='0.0.0.0', dest_port=8080,
         logger=logging.warning):
    host = dest_host if dest_host is not None else '0.0.0.0'
    port = dest_port if dest_port is not None else 8080
    try:
        conn = httplib.HTTPConnection(host, port)
        if conn is not None:
            conn.connect()
            js = None
            qp = None
            try:
                js = json.dumps(msg)
            except Exception, ex:
                
                return (httplib.UNPROCESSABLE_ENTITY,
                        reportException.report(ex, logging.error), None)
            try:
                qp = urllib.quote_plus(js, str('/'))
            except Exception, ex:
                return (httplib.UNPROCESSABLE_ENTITY,
                        reportException.report(ex, logging.error), None)
            conn.request('POST', url, qp)
            ret = conn.getresponse()
            return (ret.status, ret.reason, ret)
    except Exception, ex:
        reportException.report(ex, logger)
        return (httplib.FAILED_DEPENDENCY, None, None)
    finally:
        if conn is not None: conn.close()
        