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

import json
import httplib

from petaapan.utilities import reportException
from githubDef import *
from pssDef import *


class GithubWorker(webapp.RequestHandler):
    def post(self):
        try:
            gitpush = json.loads(self.request.body_file.getvalue())
            content_type = gitpush[CONTENT_TYPE]
            subscriber = gitpush[SUBSCRIBER]
            result = urlfetch.fetch(url=subscriber,
                                    payload=self.request.body_file.getvalue(),
                                    method=urlfetch.POST,
                                    headers={CONTENT_TYPE: content_type})
        except Exception, ex:
            self.response.set_status(httplib.UNPROCESSABLE_ENTITY,
                                     reportException.report(ex))
            return
        
        
application = webapp.WSGIApplication([('/%s' % GITHUB_TASK_URL, GithubWorker)],
                                     debug=False)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
        