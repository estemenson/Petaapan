# -*- coding: utf-8 -*-
'''
Test the Github JSON message sent after a successful git push

Created on 2010-08-27

@author: jonathan
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import unittest
import petaapan.utilities.sendJsonMsg

class GithubTest(unittest.TestCase):
       
        
    def testGithub(self):

        self.pushobj = {
                        'payload': 
                        {
                   'before':'a9b1c41c56aac56e98b5426b322cea01f170fb46',
                   'repository': 
                           {
                            'url':'http://github.com/defunkt/github',
                            'name': 'github',
                            'description': "You're lookin' at it.",
                            'watchers': 5,
                            'forks': 2,
                            'private': 0,
                            'owner': 
                               {
                                 'email': 'chris@ozmm.org',
                                 'name': 'defunkt'
                               }
                           },
                       'commits':
                           [
                               {
                                'id': '41a212ee83ca127e3c8cf465891ab7216a705f59',
                                'url': 'http://github.com/defunkt/github/commit/41a212ee83ca127e3c8cf465891ab7216a705f59',
                                'author':
                                       {
                                        'email': 'chris@ozmm.org',
                                        'name': 'Chris Wanstrath'
                                       },
                                'message': 'okay i give in',
                                'timestamp': '2008-02-15T14:57:17-08:00',
                                'added':
                                   ['filepath.rb']
                               },
                               {
                                'id': 'de8251ff97ee194a289832576287d6f8ad74e3d0',
                                'url': 'http://github.com/defunkt/github/commit/de8251ff97ee194a289832576287d6f8ad74e3d0',
                                'author':
                                   {
                                        'email': 'chris@ozmm.org',
                                        'name': 'Chris Wanstrath'
                                   },
                                'message': 'update pricing a tad',
                                'timestamp': '2008-02-15T14:36:34-08:00'
                               }
                           ],
                       'after': 'de8251ff97ee194a289832576287d6f8ad74e3d0',
                       'ref': 'refs/head/master'
                      }
                   }
        ret = petaapan.utilities.sendJsonMsg.send(self.pushobj,
                          'http://localhost:8080/%s' % self.google_app_name,
                                                  debug_level=3,
                                                  ensure_ascii=False)
        print('github test return code: %s  reason: %s',
              ret.status, ret.reason)