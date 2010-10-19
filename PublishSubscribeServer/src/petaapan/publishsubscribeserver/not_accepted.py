# -*- coding: utf-8 -*-
'''
Created on 2010-09-02

@author: jonathan
'''


from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import httplib
import logging


class MainPage(webapp.RequestHandler):
    
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.set_status(httplib.FORBIDDEN)
        logging.warning('Rejected a Get request')
        
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.set_status(httplib.FORBIDDEN)
        logging.warning('Rejected a Post request')


application = webapp.WSGIApplication([('/', MainPage), ('/.*', MainPage)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
