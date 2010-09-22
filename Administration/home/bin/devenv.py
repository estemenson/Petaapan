# -*- coding: utf-8 -*-
'''
This script sets up a development environment that supports Eclipse
and Python development using a Git repository accessed via SSH

This script will normally be invoked from .bashrc when the containing
shell is started and expects to find a bash shell environment to work in.
Created on 2010-09-21

@author: jonathan
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
from os.path import join, expanduser, isfile, isdir, pathsep
from os import environ, listdir
import subprocess
from config import Config
import devenvdef
import loadEclipse
import loadPython

_WORKSPACES = 'Workspaces'
_COMPILERS = 'Compilers'
_SSH = 'SSH'
_DEFAULT = 'Default'
_PS1 = 'PS1'
_SSHDIR = '.ssh'

def main():
    cfg = Config()
    
    current_workspace = None
    current_python = None
    home = expanduser('~')
    
    # Find out what was last used
    if cfg.has_section(_WORKSPACES):
        current_workspace = cfg.get(_WORKSPACES, _DEFAULT)
        fn = join(home, devenvdef._LAST_WORKSPACE)
        if isfile(fn):
            with open(fn, 'r') as f:
                for current_workspace in f:
                    break
        if current_workspace is None:
            print('Unable to determine a current Eclipse workspace') 

    if cfg.has_section(_COMPILERS):
        current_python = cfg.get(_COMPILERS, _DEFAULT)
        fn = join(home, devenvdef._LAST_PYTHON)
        if isfile(fn):
            with open(fn, 'r') as f:
                for current_python in f:
                    break
        if current_python is None:
            print('Unable to determine a current Python interpreter')
    
    # Set the shell prompt - This assumes that we will be running
    # in a bash shell on both Windows and Linux
    prompt = current_workspace if current_workspace is not None else '' 
    if len(prompt) > 0: prompt = prompt + ': '
    prompt = prompt + (current_python if current_python is not None else '')
    environ[_PS1] = prompt + '$'
    
    # See what the configuration file tells us about SSH keys
    # to be loaded. This code assumes we are running as a child
    # of ssh-agent so ssh-add will have someone to talk to and also
    # assumes that ssh-add is accessible via the PATH
    sshdir = join(home, _SSHDIR)
    have_sshdir = isdir(sshdir)
    if cfg.has_section(_SSH) and have_sshdir:
        for key in cfg.items(_SSH):
            fn = join(sshdir, key[0])
            if isfile(fn):
                subprocess.call(['ssh-add', fn])
    elif have_sshdir:
        for key in listdir(join(home, _SSHDIR)):
            if key[-4:] == '_rsa'  or key[-4:] == '_dsa':
                subprocess.call(['ssh-add', join(sshdir, key)])
            else:
                pass # Fillers out things that are not private keys


    if current_python is not None:    
        loadPython.load(current_python, cfg)            
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
    if current_python is not None:
        pypath = cfg.get(current_python, devenvdef._PATH) if\
             cfg.has_section(current_python) else None
        if pypath is not None:
            path = environ['PATH'].split(pathsep)
            ix = 1 if path[0] == '.' else 0
            # Remove old Python entries
#            newpath = [path.remove(p) for p in path if p.find(current_python) >= 0]
            for p in path:
                if p.find(current_python) >= 0:
                    path.remove(p)
            # Add new paths
            path.insert(ix, str(pypath))
            path.insert(ix + 1,
                        str(join(pypath,
                        'Scripts' if sys.platform == 'win32' else 'bin')))
            environ['PATH'] = pathsep.join(path)

    # Handle Eclipse startup
    if current_workspace is not None:
        loadEclipse.load(current_workspace, cfg)
    
if __name__ == '__main__':
    main()
