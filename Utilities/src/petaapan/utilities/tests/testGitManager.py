# -*- coding: utf-8 -*-
'''
Test driver for the Git Save high level command
Created on 2010-09-29

@author: jonathan
'''


from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import with_statement

import unittest
import subprocess
import stat
import Queue
from os import mkdir, chdir, getcwd,  walk, remove, rmdir, chmod
from os.path import exists, join, abspath, isdir
from petaapan.utilities.gitmanager import GitManager, SAVE, SHUTDOWN

TEST_RM_GIT = 'testRemoteGitRepo'
TEST_LOC_GIT = 'testLocalGitRepo'
PROJECTS = 'projects'
RELEASES = 'releases'
STORIES = 'stories'
SPRINTS = 'sprints'
TASKS = 'tasks'


def rmtree(base):
    if not isdir(base):
        raise OSError, '%s is not a directory' % base
    for root, dirs, files in walk(base, topdown=False):
        for name in files:
            f = join(root, name)
            chmod(f, stat.S_IWRITE)
            remove(f)
        for name in dirs:
            rmdir(join(root, name))
    rmdir(base) 
            

class Test(unittest.TestCase):

    def createFile(self, path, lines=10):
        with open(path, 'w') as f:       
            for l in range(lines):
                f.write(('*' * 50) + '\n')
                
    def modifyFile(self, path, line=5):
        with open(path, 'r+') as f:
            for l in range(line):
                f.readline()
            f.write(('+' * 50) + '\n')
            pass
                        

    def setUp(self):
        '''
        Setup and populate a local and "remote" test Git repository
        '''
        path = getcwd()
        # Get rid of any old garbage
        if exists(TEST_RM_GIT):
            rmtree(TEST_RM_GIT)
        if exists(TEST_LOC_GIT):
            rmtree(TEST_LOC_GIT)
            
        # Create a new remote repository
        args = ['git', 'init', '--bare', TEST_RM_GIT]
        subprocess.check_call(args)
        chdir(TEST_RM_GIT)
        args = ['git', 'config', 'user.name', 'Jonathan Gossage']
        subprocess.check_call(args)
        args = ['git', 'config', 'user.email', 'jgossage@xxx']
        subprocess.check_call(args)
        
        # Clone a local copy of the "remote" repository
        chdir('..')
        args = ['git', 'clone', '--no-hardlinks', abspath(TEST_RM_GIT),
                TEST_LOC_GIT]
        subprocess.check_call(args)
        chdir(TEST_LOC_GIT)
        args = ['git', 'config', 'user.name', 'Jonathan Gossage']
        subprocess.check_call(args)
        args = ['git', 'config', 'user.email', 'jgossage@xxx']
        subprocess.check_call(args)
        
        
        # Create some files in each directory
        dirs = (PROJECTS, RELEASES, STORIES, SPRINTS, TASKS)
        for d in dirs:
            mkdir(d)
            for f in range(10):
                self.createFile(join(d, 'File' + str(f)))
                
        # Checkin the content we just created and push to remote
        args = ['git', 'add'] + list(dirs)
        subprocess.check_call(args)
        args = ['git', 'commit', '-m "Initial commit"' ]
        subprocess.check_call(args)
        args = ['git', 'push', 'origin', 'master']
        subprocess.check_call(args)
        chdir('..')
        
        # Create the Git Manager that will be used for the tests
        self._queue = Queue.Queue(0)
        self._manager = GitManager(join(path, TEST_LOC_GIT),
                                   self._queue)
        self._manager.start()
        return   


    def tearDown(self):
        # Get rid of the test apparatus
        self._queue.join() # Wait for queue to flush
        self._manager.shutdown() # Wait until manager shuts down
        ret = self._queue.get(True, 60)
        self.assertTrue(ret.operation == SHUTDOWN)
        if exists(TEST_RM_GIT):
            rmtree(TEST_RM_GIT)
        if exists(TEST_LOC_GIT):
            rmtree(TEST_LOC_GIT)


    def testSave1(self):
        '''
        Add a single file to the data-store and verify that it can be saved
        Pass the file explicitly
        '''
        f = join(TEST_LOC_GIT, STORIES, 'Story1')
        self.createFile(f)
        self._manager.save([join(STORIES, 'Story1')], 'Test commit 1')
        ret = self._queue.get(True, 2400)
        self.assertTrue(ret[0] == SAVE)
        print('Stdout:')
        for l in ret[1][1]:
            print(l)
        print('Stderr:')
        for l in ret[1][2]:
            print(l)
        self.assertTrue(ret[1][0] == 0)
        if len(ret[1][3]) != 0:
            self.assertTrue(join(STORIES, 'Story1') in ret[1][3])
            
        # Add three files and modify an existing file
        # Let Git recognise the modified stuff implicitly
        
        self.createFile(join(TEST_LOC_GIT, TASKS, 'Task1'))
        self.createFile(join(TEST_LOC_GIT, PROJECTS, 'Project1'))
        self.createFile(join(TEST_LOC_GIT, SPRINTS, 'Sprint1'))
        self.modifyFile(join(TEST_LOC_GIT, STORIES, 'Story1'))
        self._manager.save(None, 'Test commit 2')
        ret = self._queue.get(True, 2400)
        self.assertTrue(ret[0] == SAVE)
        print('Stdout:')
        for l in ret[1][1]:
            print(l)
        print('Stderr:')
        for l in ret[1][2]:
            print(l)
        self.assertTrue(ret[1][0] == 0)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()