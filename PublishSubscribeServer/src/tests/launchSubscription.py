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

if __name__ != '__main__':
    from pssDef import *
    from githubDef import *
    from petaapan.utilities import sendJsonMsg

TEST_PORT = 16160

def main():
    ln = len(sys.argv)
    url = sys.argv[1]
    id = sys.argv[2]
    host = sys.argv[3] if ln > 3 else None
    port = sys.argv[4] if ln > 4 else None
    url = '%s%s' % (url, SUBACTION)
    # Try to subscribe
    status = {REQ_SUBSCRIPTION: TEST_SUBSCRIBE,
              REQ_PUBLISHER: GITHUB + '/jfgossage/Storyapp',
              REQ_PORT: TEST_PORT,
              USER_ID: id}
    
    print('About to connect to %s' % url)          
    status, reason, headers = sendJsonMsg.send(status, url,
                                               host, port)
    if status > 299:
        print('Subscription failed status %s: Reason %s' % (status, reason))
        print(headers)
        return 1
    else:
        return 0
    
if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(0, os.getcwd())
    from pssDef import *
    from githubDef import *
    from petaapan.utilities import sendJsonMsg

    ret = main()
    exit(ret)