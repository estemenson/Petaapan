# -*- coding: utf-8 -*-
'''
Created on 2010-09-24

@author: jonathan
'''


from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import httplib
import string

from pssDef import *
from githubDef import *
from petaapan.utilities import sendJsonMsg

TEST_PORT = 16160

def main():
    url = 'http://poseidon:8080/%s' % SUBACTION
    # Try to subscribe
    status = {REQ_SUBSCRIPTION: TEST_SUBSCRIBE,
              REQ_PUBLISHER: GITHUB + '/jfgossage/Storyapp',
              REQ_PORT: TEST_PORT}
              
    sendJsonMsg.send(status, url)
    
if __name__ == '__main__':
    main()