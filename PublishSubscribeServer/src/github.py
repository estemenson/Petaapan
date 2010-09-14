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

import json
import httplib
import string

from petaapan.utilities import reportException
from pssDef import *
from githubDef import *
from database import queue_pub_notifications



class MainPage(webapp.RequestHandler):
    
    
    def post(self):
        try:
            gitpush = json.loads(self.request.body_file.getvalue())
            if GITHUB_ID in gitpush:
                publication = gitpush[GITHUB_ID]
                self.response.set_status(httplib.ACCEPTED)
                repo = publication['repository']
                url = repo['url']
                publisher = string.split(url, 'http://github.com/')[1]
                content_type = self.request.headers[CONTENT_TYPE]
                queue_pub_notifications(publisher,
                                        content_type,
                                        self.request.body_file.getvalue())
            else:
                # If we don't recognise the payload, send an accepted
                # status anyway as this is likely from someone disruptive
                # and it would be a good idea to give the disrupter as
                # little information as possible
                self.response.set_status(httplib.OK)
            return
        except Exception , ex:
            self.response.set_status(httplib.UNPROCESSABLE_ENTITY,
                                     reportException.report(ex))
            return


application = webapp.WSGIApplication([('/%s' % GITHUB, MainPage)], debug=False)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
