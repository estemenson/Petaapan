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

import petaapan.utilities.sendJsonMsg
from petaapan.utilities.wanStatusDef import *

def send(status, port, url, dest_host='localhost', dest_port=8080):
    if status not in (ONLINE, TEST_ONLINE, TEST_OFFLINE, OFFLINE ):
        raise ValueError, 'Invalid application online status'
    ret = petaapan.utilities.sendJsonMsg.send({REQ_STATUS: status,
                                               REQ_PORT: port},
                                              url)
    return ret    
        