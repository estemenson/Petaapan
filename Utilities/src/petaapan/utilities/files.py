'''
Created on 2011-03-04

@author: jonathan
'''

from os.path import splitdrive, join
from os import sep, walk, remove, rmdir
def remove_tree(base, remove_root=False):
    _, tail = splitdrive(base)
    root_file = len(tail) == 1 and tail[0] == sep
    if root_file and remove_root:
        # Passed sanity check - do not accidentally remove tree that is
        # entire file system
        if remove_root: print('Removing root file system')
        for root, dirs, files in walk(base, topdown=False):
            for name in files:
                remove(join(root, name))
            for name in dirs:
                rmdir(join(root, name))
