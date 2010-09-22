# -*- coding: utf-8 -*-
'''
Loads a specified Eclipse workspace
Created on 2010-09-21

@author: jonathan
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
import subprocess
from os.path import dirname, expanduser, join
from config import Config
import devenvdef


def load(req, cfg):
    if cfg.has_section(req):
        p = cfg.get(req, devenvdef._PATH)
        ws = cfg.get(req, devenvdef._WORKSPACE)
        # Starts Eclipse as an asynchronous process
        subprocess([p, '-nosplash', '-data',  ws],
                   cwd=dirname(p))
        # Update the last used Eclipse workspace record
        fd = open(join(expanduser('~'),
                       devenvdef._LAST_WORKSPACE),
                  'w')
        fd.write(req)
        fd.close()
    
    
def main():
    load(sys.argv[1], Config())
    
if __name__ == '__main__':
    main()
