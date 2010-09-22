# -*- coding: utf-8 -*-
'''
This script launches the Eclipse/Python based
development environment.

It starts by starting ssh-agent which will run an
instance of the bash shell as a child. The script
that does the heavy lifting in setting up the environment
is run from .bashrc thus leaving an interaactive shell
that is an integral part of the development
environment.
 
Created on 2010-09-21

@author: jonathan
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import subprocess
from os import environ

def main():
    environ['AGIMAN_STARTUP'] = '1'
    subprocess(['ssh-agent', 'bash', '-i'])
    
    
if __name__ == '__main__':
    main()
    pass