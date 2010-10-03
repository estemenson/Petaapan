# -*- coding: utf-8 -*-
'''
Handles the interface to the Git SCM and provides a high level
API to use Git as a versioned file manager
Created on 2010-09-30

@author: jonathan
'''


from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import with_statement

import subprocess
import threading
import Queue
import string
from os.path import relpath, abspath, isabs
import os

from petaapan.utilities import reportException

GIT_SAVE = 'GitSave'
SHUTDOWN = 'Shutdown'
SAVE = 'Save'
COMMIT = 'Commit'
MV = 'Mv'
RM = 'Rm'
    

class GitManager(threading.Thread):
    def __init__(self, localrepo, response_queue):
        '''
        Constructor
        localrepo:       path to the directory that contains the local
                         Git repository
        response_queue:  the queue that will be used to send operation
                         results to the caller
        
        Sets up the queue that is used to communicate between the callers
        and the thread that performs the Git operations
        '''
        self._localrepo = localrepo
        self._response_queue = response_queue
        super(GitManager, self).__init__(None, None, 'GitManager')
        if self._localrepo is not None:
            self._internalQueue = Queue.Queue(0)
        
    def shutdown(self):
        '''
        Shutdown the GitManager
        Sends a shutdown message on the internal queue to the Git manager
        '''
        if self._localrepo is not None:
            self._internalQueue.put((SHUTDOWN, (None)), True, 60)
        
        
    def runCommand(self, args):
        _consoleStdout = []
        _consoleStderr = []
        _commits = set([])
        _result = 0
        p = subprocess.Popen(args, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             cwd=self._localrepo)
        stdout, stderr = p.communicate()
        _result = p.wait()
        if stdout is not None and len(stdout) != 0:
            _consoleStdout += string.split(stdout, '\n')
        if stderr is not None and len(stderr) != 0:
            _consoleStdout += string.split(stderr, '\n')
        return (_result, _consoleStdout, _consoleStderr, _commits)
        
    def save(self, files, message):
        '''
        Puts changed files into the local Git repository and pushes them
        to the remote repository if possible. This method is invoked
        by our users
        
        files:   list of objects to be saved
                 if None or the list is empty all new and modified objects
                 will be saved, otherwise only the user specified objects will
                 be saved
        message: the commit message to be used for the local commit
        '''
        if self._localrepo is not None:
            self._internalQueue.put((SAVE, (files, message)), False)

            
    def commit(self, files, message):
        '''
        Commits objects to the local repository without pushing them
        to the remote repository. This method is invoked by our users
        
        files:   list of objects to be saved
                 if None or the list is empty all new and modified objects
                 will be saved, otherwise only the user specified objects will
                 be saved
        message: the commit message to be used for the local commit
        '''
        if self._localrepo is not None:
            self._internalQueue.put((COMMIT, (files, message)), False)

            
    def mv(self, old, new):
        '''
        Renames or moves an object within the local repository or
        in the local file system if the local repository is not
        available
        
        old:   Old name
        new:   New name
        '''
        self._internalQueue.put((MV, (old, new)), False)

            
    def rm(self, file):
        '''
        Removes an object within the local repository or
        in the local file system if the local repository is not
        available
        
        file:    object to be removed
        '''
        self._internalQueue.put((RM, (file)), False)
        
        
    def run(self):
        data = threading.local()
        data.do_shutdown = False

        # The internal command processing methods are nested here so
        # that they have access to the thread local data        
        def internalSave(self, args):
            '''
            This method is used internally within the GitManager thread to
            actually perform the requested work
            '''
            files, message = args
            try:
                data.ret = self.doGitAdd(files)
                if data.ret[0] != 0:
                    return
                data.ret = self.doGitCommit(message)
                if data.ret[0] != 0:
                    return
                data.ret = self.doGitFetch()
                if data.ret[0] != 0:
                    return
                data.ret = self.doGitMerge()
                if data.ret[0] != 0:
                    return
                data.ret = self.doGitPush()
                return
            finally:
                self._response_queue.put((SAVE, data.ret), False)
                data.ret = None

        
        def internalShutdown(self, args):
            data.doShutdown = True
            self._response_queue.put((SHUTDOWN))
            data.ret = None
            
        def internalCommit(self, args):
            files, message = args
            try:
                data.ret = self.doGitAdd(files)
                if data.ret[0] != 0:
                    return
                data.ret = self.doGitCommit(message)
                return
            finally:
                self._response_queue.put((COMMIT, data.ret), False)
                data.ret = None
                
        def internalMv(self, args):
            old, new = args
            try:
                data.ret = self.doGitMv(old, new)
            finally:
                self._response_queue.put((MV, data.ret), False)
                data.ret = None
                
        def internalRm(self, args):
            try:
                data.ret = self.doGitRm(args[0])
            finally:
                self._response_queue.put((RM, data.ret), False)
                data.ret = None
                
            
            
        data.dispatcher = {SAVE : internalSave,
                           SHUTDOWN: internalShutdown,
                           COMMIT: internalCommit,
                           MV: internalMv,
                           RM: internalRm}
        while not data.do_shutdown:
            args = self._internalQueue.get(True)
            if args[0] in data.dispatcher:
                data.dispatcher[args[0]](self, args[1])
        return
            
    def doGitAdd(self, files):
        args = ['git', 'add']
        if files is None or len(files) == 0:
            # User wants everything saved - modified and new objects
            args.append('--all')
        else:
            # User wants a specified list of objects saved
            for f in files:
                args += self.normalizePath(f) 
        return self.runCommand(args)
    
    def doGitCommit(self, message):
        args = ['git', 'commit', '-m', message]
        return self.runCommand(args)

    def doGitFetch(self):
        args = ['git', 'fetch']
        return self.runCommand(args)

    def doGitMerge(self):
        args = ['git', 'merge', '--commit', '-m', 'Merged pull from remote',
                'remotes/origin/master']
        return self.runCommand(args)
    
    def doGitPush(self):
        args = ['git', 'push']
        return self.runCommand(args)
    
    def doGitMv(self, old, new):
        if self._localrepo is not None:
            args = ['git','mv', self.normalizePath(old),
                    self.normalizePath(new)]
            return self.runCommand(args)
        else:
            try:
                _old = abspath(old) if not isabs(old) else old
                _new = abspath(new) if not isabs(new) else new
                os.rename(_old, _new)
                return (0, [], [], set([]))
            except Exception, ex:
                return (1, [], reportException.report(ex), set([])) 
    
    def doGitRm(self, file):
        if self._localrepo is not None:
            args = ['git','rm', self.normalizePath(file)]
            return self.runCommand(args)
        else:
            try:
                _file = abspath(file) if not isabs(file) else file
                os.remove(_file)
                return (0, [], [], set([]))
            except Exception, ex:
                return (1, [], reportException.report(ex), set([])) 
            
    def normalizePath(self, path):
        '''
        Converts path to a path relative to the local repository base
        '''
        return relpath(path, self._localrepo)
