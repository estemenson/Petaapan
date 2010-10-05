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
            return self._response_queue.get(True, 60)
        
        
    def runCommand(self, cmd, ret, args):
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
            for l in string.split(stdout, '\n'):
                _consoleStdout.append(cmd + ': ' + l)
        _consoleStdout.append('%s terminated with code %i' % (cmd, _result)) 
        if stderr is not None and len(stderr) != 0:
            for l in string.split(stderr, '\n'):
                _consoleStderr.append(cmd + ': ' + l)
        if (_result > 0 and _result > ret[0]):
            ret[0] = _result
        ret[1] += _consoleStdout
        ret[2] += _consoleStderr
        
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
            data.ret = [0, [], [], set([])]
            try:
                self.doGitAdd(data.ret, files)
                if data.ret[0] != 0:
                    return
                self.doGitCommit(data.ret, message)
                if data.ret[0] != 0:
                    return
                self.doGitFetch(data.ret)
                if data.ret[0] != 0:
                    return
                self.doGitMerge(data.ret)
                if data.ret[0] != 0:
                    return
                self.doGitPush(data.ret)
                return
            finally:
                self._response_queue.put((SAVE, data.ret), False)
                data.ret = None

        
        def internalShutdown(self, args):
            data.doShutdown = True
            self._response_queue.put((SHUTDOWN,
                                      [0, ['Asynchronous services shutdown'],
                                       [], set([])]))
            data.ret = None
            
        def internalCommit(self, args):
            files, message = args
            data.ret = [0, [], [], set([])]
            try:
                self.doGitAdd(data.ret, files)
                if data.ret[0] != 0:
                    return
                self.doGitCommit(data.ret, message)
                return
            finally:
                self._response_queue.put((COMMIT, data.ret), False)
                data.ret = None
                
        def internalMv(self, args):
            old, new = args
            data.ret = [0,[],[], set([])]
            try:
                self.doGitAdd(data.ret, None)
                if data.ret[0] != 0:
                    return
                self.doGitCommit(data.ret, 'Cleanup before Git mv')
                if data.ret[0] != 0:
                    return
                self.doGitMv(data.ret, old, new)
            finally:
                self._response_queue.put((MV, data.ret), False)
                data.ret = None
                
        def internalRm(self, args):
            data.ret = [0, [], [], set([])]
            try:
                self.doGitAdd(data.ret, None)
                if data.ret[0] != 0:
                    return
                self.doGitCommit(data.ret, 'Cleanup before Git rm')
                if data.ret[0] != 0:
                    return
                self.doGitRm(data.ret, args)
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
            
    def doGitAdd(self, ret, files):
        args = ['git', 'add']
        if files is None or len(files) == 0:
            # User wants everything saved - modified and new objects
            args.append('--all')
        else:
            # User wants a specified list of objects saved
            if not isinstance(files, list):
                files = [files]
            args += files 
        self.runCommand('Git add', ret, args)
    
    def doGitCommit(self, ret, message):
        '''
        We need to see if there is a need to run the Git commit command
        This is because Git commit considers it an error
        if you try to commit when there is nothing to commit.
        Accordingly we run the Git status command and parse the output
        to see if it is necessary to run Git commit
        '''
        args = ['git', 'status']
        iret = [0, [], [], set([])]
        self.runCommand('Git status', iret, args)
        if iret[0] != 0:
            ret[0] = iret[0]
            ret[1] += iret[1]
            ret[2] += iret[2]
            return # Status command failed
        doCommit = True
        for l in iret[1]:
            if string.find(l, 'nothing to commit') >= 0:
                doCommit = False
                break
        if doCommit:
            args = ['git', 'commit', '-m', message]
            self.runCommand('Git commit', ret, args)

    def doGitFetch(self, ret):
        args = ['git', 'fetch']
        self.runCommand('Git fetch', ret, args)

    def doGitMerge(self, ret):
        args = ['git', 'merge', '--commit', '-m', 'Merged pull from remote',
                'remotes/origin/master']
        self.runCommand('Git merge', ret, args)
    
    def doGitPush(self, ret):
        args = ['git', 'push']
        self.runCommand('Git push', ret, args)
    
    def doGitMv(self, ret, old, new):
        if self._localrepo is not None:
            args = ['git','mv', old, new]
            self.runCommand('Git mv', ret, args)
        else:
            try:
                os.rename(old, new)
            except Exception, ex:
                ret[0] = 1
                ret[1].append(reportException.report(ex))
    
    def doGitRm(self, ret, file):
        if self._localrepo is not None:
            args = ['git','rm', file]
            self.runCommand('Git rm', ret, args)
        else:
            try:
                os.remove(file)
            except Exception, ex:
                ret[0] = 1
                ret[1].append(reportException.report(ex))
                
    def doGitStatus(self, ret): 
        args = ['git', 'status']
