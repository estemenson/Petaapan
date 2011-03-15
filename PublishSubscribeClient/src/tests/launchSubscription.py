# -*- coding: utf-8 -*-
'''
Created on 2010-09-24

@author: jonathan
'''


from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from publishsubscribeserver.pssDef import REQ_SUBSCRIPTION
from publishsubscribeserver.pssDef import TEST_SUBSCRIBED, REQ_PORT
from publishsubscribeserver.pssDef import REQ_PUBLISHER, USER_ID
from publishsubscribeserver.pssDef import SUBSCRIBER_DNS, SUBACTION
from publishsubscribeserver.pssDef import SUBSCRIBER_PORT, FIRST_NAME
from publishsubscribeserver.pssDef import MIDDLE_NAME, LAST_NAME
from publishsubscribeserver.githubDef import GITHUB
from petaapan_utilities import sendJsonMsg

TEST_PORT = 16160

def main():
    ln = len(sys.argv)
    url = sys.argv[1]
    id = sys.argv[2]
    host = sys.argv[3] if ln > 3 else None
    port = sys.argv[4] if ln > 4 else None
    subscriberDns = sys.argv[5] if ln > 5 else 'poseidon.petaapan.org'
    subscriberPort = sys.argv[6] if ln > 6 else TEST_PORT
    firstName = sys.argv[7] if ln > 7 else 'Jonathan'
    middleName = sys.argv[8] if ln > 8 else 'Frederick'
    lastName = sys.argv[9] if ln > 9 else 'Gossage'
    url = '%s%s' % (url, SUBACTION)
    # Try to subscribe
    status = {REQ_SUBSCRIPTION: TEST_SUBSCRIBED,
              REQ_PUBLISHER: GITHUB + '/jfgossage/Storyapp',
              REQ_PORT: TEST_PORT,
              USER_ID: id,
              SUBSCRIBER_DNS: subscriberDns,
              SUBSCRIBER_PORT: subscriberPort}
    if firstName is not None:
        status[FIRST_NAME] = firstName
        if middleName is not None:
            status[MIDDLE_NAME] = middleName
            if lastName is not None:
                status[LAST_NAME] = lastName
    
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

    ret = main()
    exit(ret)