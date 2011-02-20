# -*- coding: utf-8 -*-
'''
Accepts webhook based notifications from github.com
Compatible with Python 2.5 or later

Created on 2101-09-10

@author: jonathan
'''


from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson

import httplib
import string
import urllib
import logging
logging.basicConfig(level=logging.DEBUG)
doLog = {logging.CRITICAL: logging.critical,
         logging.ERROR: logging.error,
         logging.WARNING: logging.warning,
         logging.INFO: logging.info,
         logging.DEBUG: logging.debug}

from petaapan.utilities import reportException
from petaapan.publishsubscribeserver.githubDef import GITHUB
from petaapan.publishsubscribeserver.database import queue_pub_notifications



class MainPage(webapp.RequestHandler):
        
    def doReturn(self, level, status, msg):
        doLog[level](msg)
        self.response.set_status(status, msg)
    
    
    def post(self):
        try:
            str1 = unicode(urllib.unquote_plus(self.request.body_file.getvalue()))
            if string.find(str1, 'payload=') >= 0:
                msg = string.split(str1, 'payload=')[1]
                gitpush = simplejson.loads(msg)
                self.response.set_status(httplib.OK)
                repo = gitpush['repository']
                url = repo['url']
                publisher = GITHUB + '/' + string.split(url, 'http://github.com/')[1]
                queue_pub_notifications(publisher, gitpush)
            else:
                # If we don't recognise the payload, send an accepted
                # status anyway as this is likely from someone disruptive
                # and it would be a good idea to give the disrupter as
                # little information as possible
                logging.warning('''Received invalid message, theoretically from Github.\n'''
                                '''   Headers; %s\n   Payload: %s''' % self.headers, str1)
                self.response.set_status(httplib.OK)
            return
        except Exception , ex:
            self.doReturn(logging.ERROR, httplib.UNPROCESSABLE_ENTITY,
                           reportException.report(ex))
            return


application = webapp.WSGIApplication([('/%s' % GITHUB, MainPage)],
                                     debug=False)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
