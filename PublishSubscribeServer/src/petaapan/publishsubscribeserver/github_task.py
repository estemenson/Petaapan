# -*- coding: utf-8 -*-
'''

Send newly published content to a subscriber
Currently runs in a GAE task queue
Compatible with Python 2.5 or later

Created on 2010-09-13

@author: jonathan
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
from django.utils import simplejson

import httplib
import urllib
import logging
import time

from petaapan.utilities import reportException
from petaapan.publishsubscribeserver.githubDef import *
from petaapan.publishsubscribeserver.pssDef import *


class GithubWorker(webapp.RequestHandler):
    def post(self):
        ret = httplib.OK
        try:
            gitpush = simplejson.loads(\
                        urllib.unquote_plus(self.request.body_file.getvalue()))
            subscriber = gitpush[SUBSCRIBER]
            logging.debug('Sending Github notification to %s at %f'\
                          % (subscriber, time.clock()))
            result = urlfetch.fetch(url=subscriber,
                                    payload=self.request.body_file.getvalue(),
                                    method=urlfetch.POST, deadline=10)
            logging.debug(\
                     'Github transmission to %s completed with code %i at %s'\
                           % (result.final_url if result.final_url else subscriber,
                              result.status_code,
                              time.clock()))
            ret = result.status_code
            return
        except Exception, ex:
            logging.debug('Github transmission to %s failed at %f'\
                          % (subscriber, time.clock()))
            reportException.report(ex, logging.error)
            return
        finally:
            self.response.set_status(ret)
        
        
application = webapp.WSGIApplication([(GITHUB_TASK_URL, GithubWorker)],
                                     debug=False)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
        