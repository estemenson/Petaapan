# -*- coding: utf-8 -*-
'''
Created on 2010-07-01

@author: Jonathan Gossage
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import os

class EnvironmentPath(object):
    '''
    This class provides methods to manage the PATH environment variable
    provided by the Windows and Unix like operating systems. The PATH variable
    is maintained by the operating system as an OS specific delimiter separated
    list of strings representing paths to locations in the operating system that
    are to be searched for executable programs or scripts to be run. Paths may have
    other environment variables embedded within them which will need to be evaluated,
    possibly recursively, before the path strings become usable.
    
    This class provides the following capabilities:
    1. Iterate over the list of paths contained in the PATH environment variable.
    2. Determine if a given executable or script can be found via the PATH environment
       variable.
    3. Determine whether the caller is authorised to execute a program or script.
    '''


    def __init__(self, environment = os.environ, pathsep = os.path.pathsep, dirsep = os.path.sep):
        '''
        Constructor
        '''
        # Build the path table
        self.pathTable = []
        parstr = environment['PATH'].partition(pathsep)
        while parstr[0] != '':
            # Sanitise the path
            self.pathTable.append(parstr[0].strip().rstrip(dirsep))
            # Extract the next path
            parstr = parstr[2].partition(pathsep)

    def iterator(self):
        return self.pathTable.iter()

    def findPath(self, executable, flags):
        for p in self.pathTable:
            p = os.path.join(p, executable)
            if os.access(p, flags):
                return p
        return ''


    def exists(self, executable):
        '''
        Returns True if executable exists, False otherwise
        '''
        spl = os.path.split(executable)
        if spl[1] == '':
            return False # No executable supplied
        if spl[0] != '': # We have a path - make it absolute and see if it exists
            return os.access(os.path.abspath(executable), os.F_OK)
        # Look for executable on path
        return self.findPath(executable, os.F_OK) != ''

    def runnable(self, executable):
        spl = os.path.split(executable)
        if spl[1] == '':
            return False # No executable supplied
        if spl[0] != '': # We have a path - make it absolute and see if it exists
            return os.access(os.path.abspath(executable), os.X_OK)
        return self.findPath(executable, os.X_OK) != ''

    def getPath(self, executable):
        spl = os.path.split(executable)
        if spl[1] == '':
            return '' # No executable supplied
        p = os.path.abspath(executable)
        if spl[0] != '' & os.access(p, os.X_OK):
            return p;
        return self.findPath(executable, os.X_OK)


