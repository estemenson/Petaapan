# -*- coding: utf-8 -*-
'''
Makes a specified Python interpreter the default interpreter
Created on 2010-09-21

@author: jonathan
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
import subprocess
from os import environ
from os.path import dirname, expanduser, join, pathsep
from config import Config
import devenvdef


def load(req, cfg):
    # Setup Python
    # We do this as follows:
    # assume that the standard path has entries for pythonxx and
    # pythonxx/[Scripts | bin]
    # First remove them from the path
    # Also, MSYS puts '.' as the first entry in the PATH to emulate
    # the Windows command line behaviour so remember if it is there
    # Now rebuild the path as follows:
    # First entry is '.' followed by the path to Python and
    # the path to the Python scripts directory
    pypath = cfg.get(req, devenvdef._PATH) if\
         cfg.has_section(req) else None
    if pypath is not None:
        path = environ['PATH'].split(pathsep)
        ix = 1 if path[0] == '.' else 0
        # Remove old Python entries
        for p in path:
            if p.find(req) >= 0:
                path.remove(p)
        # Add new paths
        path.insert(ix, str(pypath))
        path.insert(ix + 1,
                    str(join(pypath,
                    'Scripts' if sys.platform == 'win32' else 'bin')))
        environ['PATH'] = pathsep.join(path)
        
        # Update record of last used Python interpreter
        fd = open(join(expanduser('~'), devenvdef._LAST_PYTHON), 'w')
        fd.write(req)
        fd.close()
    
    
def main():
    load(sys.argv[1], Config())

if __name__ == '__main__':
    pass