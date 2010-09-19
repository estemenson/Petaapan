# -*- coding: utf-8 -*-
'''
Contains assorted general purpose validation classes used when collecting
arguments from the command line and configuration files.

Created on 2010-09-16

@author: jonathan
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from os.path import isdir, isfile, exists
from urllib2 import urlopen, URLError
import logging

import petaapan.utilities.argparse

def ValidateUrl(url):
    result = logging.NOTSET
    c = None
    errmsg = []
    try:
        c = urlopen(url)
        return (result, errmsg)
    except URLError, ex:
        return BadUrl(ex, url)        
    except ValueError, ex:
        return BadUrl(ex, url)
    finally:
        if c is not None: c.close()


def BadUrl(ex, url):
        errmsg = []
        errmsg.append(\
        "%s is an invalid, non-existent or currently inaccessible URL" % (url))
        errmsg.append(unicode(ex))
        return (logging.ERROR, errmsg)

def ValidateExistingDirectory(path):
        result = logging.NOTSET
        errmsg = []
        if isdir(path) and exists(path):
            return (result, errmsg)
        else:
            result = logging.ERROR
            errmsg.append(\
               '%s must be an existing directory on the current path' % (path))
            return (result, errmsg)


def ValidateExistingFile(path):
        result = logging.NOTSET
        errmsg = []
        if isfile(path) and exists(path):
            return (result, errmsg)
        else:
            result = logging.ERROR
            errmsg.append(\
               '%s must be an existing file on the current path' % (path))
            return (result, errmsg)
