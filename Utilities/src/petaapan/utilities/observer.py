# -*- coding: utf-8 -*-'''
'''
Created on 2010-09-23

@author: jonathan
'''



from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


class Observer(object):


    def __init__(self, action):
        self._action = action
        
    def __call__(self):
        self._action()
        
    def setAction(self, action):
        self._action = action