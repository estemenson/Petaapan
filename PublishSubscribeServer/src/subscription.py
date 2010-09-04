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
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app

import json
import httplib
import string

from petaapan.utilities import reportException
from petaapan.utilities.wanStatusDef import *


class Subscriber(db.Expando):
    first_name = db.StringProperty(indexed=False)
    middle_name = db.StringProperty(indexed=False)
    last_name = db.StringProperty(indexed=False)
    email_address = db.StringProperty(indexed=False)
    google_id = db.UserProperty(required=True, indexed=True)
    user_ip = db.StringProperty(required=True, indexed=True)
    user_port = db.IntegerProperty(required=True)    
    status = db.IntegerProperty(default=UNSUBSCRIBE,
                                choices=set([UNSUBSCRIBE, SUBSCRIBE]),
                                required=True, indexed=True)
    
    
class MainPage(webapp.RequestHandler):
    ONLINE_LIST_KEY = 'Subscribers'
    
    def post(self):
        try:
            ipaddr = self.request.remote_addr
            req = json.loads(self.request.body_file.getvalue())
            if REQ_SUBSCRIPTION not in req:
                self.response.set_status(httplib.PRECONDITION_FAILED,
                                 'No subscription status provided in request')
                return
            testing = False
            status = req[REQ_SUBSCRIPTION]
            port = req[REQ_PORT]
            if status == TEST_SUBSCRIBE:
                status = SUBSCRIBE
                testing = True
            elif status == TEST_UNSUBSCRIBE:
                status = UNSUBSCRIBE
                testing = True
            
            # Make sure this user is registered at Google and logged on
            guser = users.get_current_user()
            if not guser:
                if not testing:
                    self.response.set_status(httplib.PRECONDITION_FAILED,
         'You are not logged on to Google via your Google account or OpenId')
                    return
                else:                   
                    guser = users.User(email='jgossage@gmail.com')
                
            
            # Get online user list from memcache if it is there, otherwise
            # load it from the data store
            
            cache = memcache.Client()
            ul = cache.get(MainPage.ONLINE_LIST_KEY)
            if ul is None:
                ul = self.load_online_users()
                
            
            # See if user in cache
            # If not add user to  cache
            uid = guser.user_id()
            if testing and uid is None:
                uid = string.split(guser.email(),'@')[0]
            key = uid+ipaddr+str(port)
            cuser = ul[key] if key in ul else None
            if cuser is None:
                cuser = Subscriber(google_id=guser, status=status,
                                user_ip=ipaddr, user_port=port)
                cuser.put()
                ul[key] = cuser
                cache.set(MainPage.ONLINE_LIST_KEY, ul)
            
            # If user is coming online but is already recorded as online
            # simply set error code and return
            
            # If user is coming online update
            # the user entity in the data store to show online status
            if status == SUBSCRIBE:
                if cuser.status != SUBSCRIBE:
                    cuser.status = SUBSCRIBE
                    cuser.put() 
                    cache.set(MainPage.ONLINE_LIST_KEY, ul)
                    
            # If user is going offline update                   
            # the user entity in the data store to show offline status
            elif status == UNSUBSCRIBE:
                if cuser.status != UNSUBSCRIBE:
                    cuser.status = UNSUBSCRIBE
                    cuser.put() 
                    cache.set(MainPage.ONLINE_LIST_KEY, ul)
            else:
                self.response.set_status(httplib.NOT_ACCEPTABLE,
                                         'Urecognized status notification')
                return
            
            # Normal return
            self.response.set_status(httplib.ACCEPTED,
                                     'Status set to %s' % TEST_SUBSCRIBED
                                     if status == SUBSCRIBE
                                     else TEST_UNSUBSCRIBED )
            
        except Exception , ex:
            self.response.set_status(httplib.UNPROCESSABLE_ENTITY,
                                     reportException.report(ex))
            return
            
    def load_online_users(self):
        query = db.GqlQuery("SELECT * FROM Subscriber WHERE status = :1",
                            SUBSCRIBE)
        ul = {}
        for user in query:
            ul[user.google_id.user_id() + user.user_ip + str(user.user_port)] = user
        return ul
        


application = webapp.WSGIApplication([('/%s' % SUBACTION, MainPage)],
                                     debug=False)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
