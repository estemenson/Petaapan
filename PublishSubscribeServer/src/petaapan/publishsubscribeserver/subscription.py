# -*- coding: utf-8 -*-
'''
Manages recording of user presence in a distributed environment
Compatible with Python 2.5 or later

Created on 2010-08-28

@author: jonathan
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson

import httplib
import urllib
import string
import logging
logging.basicConfig(level=logging.DEBUG)

from petaapan.utilities import reportException
from petaapan.publishsubscribeserver.pssDef import *
from petaapan.publishsubscribeserver.database import Subscriber, load_online_subscribers
from petaapan.publishsubscribeserver.cache import GacCache

doLog = {logging.CRITICAL: logging.critical,
         logging.ERROR: logging.error,
         logging.WARNING: logging.warning,
         logging.INFO: logging.info,
         logging.DEBUG: logging.debug}
    
    
class MainPage(webapp.RequestHandler):
    
    def __init__(self):
        self.cache = GacCache()
        
    def doReturn(self, level, status, msg):
        doLog[level](msg)
        self.response.set_status(status, msg)
    
    def post(self):
        try:
            req = simplejson.loads(urllib.unquote_plus(\
                                            self.request.body_file.getvalue()))
            if REQ_SUBSCRIPTION not in req or REQ_PUBLISHER not in req:
                self.doReturn(logging.WARNING, httplib.PRECONDITION_FAILED,
                    'No or incomplete subscription status provided in request')
                return
            status = req[REQ_SUBSCRIPTION]
            publisher = req[REQ_PUBLISHER]
            port = req[REQ_PORT]
            testing = True if TESTING in req else False
            
            # Make sure this user is registered at Google and logged on
            guser = users.get_current_user()
            if not guser:
                guser = users.User(email=req[USER_ID])
                if guser.user_id() == None and not testing:
                    self.doReturn(logging.WARNING, httplib.NOT_ACCEPTABLE,
                                  'Urecognized Google user')
                    return
                        
                
            
            # Get online user list from memcache if it is there, otherwise
            # load it from the data store
            
            ul = self.cache.load_cache(publisher, load_online_subscribers)
                
            
            # See if user in cache
            # If not add user to  cache
            uid = guser.user_id()
            if testing and uid is None:
                uid = string.split(guser.email(),'@')[0]
            key = uid+req[SUBSCRIBER_DNS]+str(port)
            cuser = ul[key] if key in ul else None
            if cuser is None:
                cuser = Subscriber(google_id=guser, status=status,
                                   user_ip=req[SUBSCRIBER_DNS], user_port=port,
                                   email_address=guser.email(),
                                   publisher=publisher
#                                   first_name=req[FIRST_NAME],
#                                   middle_name=req[MIDDLE_NAME],
#                                   last_name=req[LAST_NAME]
                                   )
                self.cache.update(publisher, key, cuser)
            
            # If user is coming online update
            # the user entity in the data store to show online status
            if status == SUBSCRIBE:
                if cuser.status != SUBSCRIBE:
                    cuser.status = SUBSCRIBE
                    self.cache.update(publisher, key, cuser)
                    
            # If user is going offline update                   
            # the user entity in the data store to show offline status
            elif status == UNSUBSCRIBE:
                if cuser.status != UNSUBSCRIBE:
                    cuser.status = UNSUBSCRIBE
                    self.cache.update(publisher, key, cuser)
            else:
                self.doReturn(logging.WARNING, httplib.NOT_ACCEPTABLE,
                              'Urecognized status notification')
                return
            
            # Normal return
            self.doReturn(logging.DEBUG, httplib.ACCEPTED,
                          'Status set to %s' % TEST_SUBSCRIBED
                                               if status == SUBSCRIBE
                                               else TEST_UNSUBSCRIBED )
            return
            
        except Exception , ex:
            self.doReturn(logging.ERROR, httplib.UNPROCESSABLE_ENTITY,
                          reportException.report(ex))
            return
            
        


application = webapp.WSGIApplication([('/%s' % SUBACTION, MainPage)],
                                     debug=False)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
