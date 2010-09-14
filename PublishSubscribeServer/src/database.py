# -*- coding: utf-8 -*-
'''
Provides GAC database management support
Compatible with Python 2.5 or later

Created on 2010-09-10

@author: jonathan
'''


from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement

from google.appengine.ext import db
from google.appengine.api.labs import taskqueue
from pssDef import *
from githubDef import *

import json

subscribers_to_pub\
    = "SELECT * FROM Subscriber WHERE status = :1 AND publisher = :2"

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
    publisher = db.StringProperty(required=True, indexed=True)
    
    
def load_online_subscribers(publisher):
    query = db.GqlQuery(subscribers_to_pub, SUBSCRIBE, publisher)
    ul = {}
    for subscriber in query:
        ul[subscriber.google_id.user_id() + subscriber.user_ip + str(subscriber.user_port)]\
            = subscriber
    return ul


def queue_pub_notifications(publisher, content_type, payload):
    query = db.GqlQuery(subscribers_to_pub, SUBSCRIBE, publisher)
    for subscriber in query:
        taskqueue.add(url=GITHUB_TASK_URL,
                      params=json.dumps({SUBSCRIBER: '%s:%s' % (subscriber.user_ip,
                                                                subscriber.user_port),
                                         CONTENT_TYPE: content_type,
                                         GITHUB_ID : payload[GITHUB_ID]}))
