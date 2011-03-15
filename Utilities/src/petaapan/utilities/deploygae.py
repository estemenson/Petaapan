'''
Created on 2011-02-23

Runs any combination of the various deployment tasks

The following tasks are supported

* Create a fully populated deployment directory
* Update an existing deployment directory
* Test the contents of a deployment directory without using Eclipse
* Upload a deployment to Google Apps

@author: jonathan
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
from os.path import split, realpath, isfile, isdir, join
from os import walk

from petaapan.utilities.argparse import Action, ArgumentParser, SUPPRESS,\
                                        ArgumentError

CREATE = 'create'
UPDATE = 'update'
TEST = 'test'
UPLOAD = 'upload'

base_directory = None
base_app = None
deploy_path = None

def main():
    try:
        config = getConfig(sys.argv)
        
        
        if config.create:
            createDeployment(config)
        elif config.update:
            updateDeployment(config)
            
        if config.test:
            testDeployment(config)
            
        if config.upload:
            uploadDeployment(config)
            
    except Exception, e:
        print(e.str())
        
class DeployChecker(Action):
    '''Validates a deployment path'''
    def __call__(self, parser, namespace, values, option_string = None):
        v = None
        if isdir(values[0]): # We have an existing directory
            v = (True, values[0])
        elif isfile(values[0]): # We have an existing file
            ArgumentError(self,
                          'Deployment path must end in a directory, '
                                 'not a file.')
        else: # Deployment directory does not exist yet
            v = (False, values[0])
        setattr(namespace, self.dest, v )
            
class StaticChecker(Action):
    def __call__(self, parser, namespace, values, option_string = None):
        v = []
        for f in values:
            if isfile(f) or isdir(f):
                v.append(f)
            else: # File or directory not found
                ArgumentError(self,
                              'Unable to find static file or directory'
                                     ' %s' % (f))
        setattr(namespace, self.dest, v)
        
class PackageChecker(Action):
    def __call__(self, parser, namespace, values, option_string = None):
        v = []
        for d in values:
            if isdir(d): # We may have a package directory
                if isfile(join(d,'__init__.py')):   # We definitely have
                                                    # a package directory
                    v.append(d)
            else: # Not a package directory or non-existent
                ArgumentError(self,
                              'Non-existent directory or not a '
                                     'Python package directory: %s ' % (d))
        setattr(namespace, self.dest, v)
        
def getConfig(args=None):
    '''
    Parse the command line arguments to setup the configuration
    for this invocation
    '''
    if args == None:
        args = []
    if len(args) == 0:
        args.append('--version')
        
    _, base_app = split(realpath(sys.argv[0]))
    parser = ArgumentParser(prog='[python] '\
                                + base_app,
                            description=\
                            'Google App Engine deployment tool')
    parser.add_argument('--version', action='version',\
                        version='%(prog)s 0.1.0', help=\
                        'Display the version of the deployer')
    subparsers = parser.add_subparsers(help='sub-command help')
    cmd_create = subparsers.add_parser('create', help=\
    'Requests the creation of a new deployment directory.'
    'If the directory exists it is deleted and a new one is created')
    cmd_create.add_argument('deploy', action=DeployChecker, help=\
                        'Defines the path to the deployment directory')
    cmd_create.add_argument('-s', '--static', action=StaticChecker, nargs='*',
                            default=SUPPRESS, help=\
   'List of files and directories containing static '
   'content to be displayed by the deployed application')
    cmd_create.add_argument('-p', '--package', action=PackageChecker, nargs='+',
                            required=True,
                            help=\
    'List of paths to the package directories to be deployed. '
    'This argument is required')
    cmd_update = subparsers.add_parser('update', help=\
   'Requests the updating of an existing deployment directory.'
   'Only files newer than the ones in the deployment '
   'directory are added/updated in the directory.')
    cmd_update.add_argument('deploy', action=DeployChecker, help=\
                        'Defines the path to the deployment directory')
    cmd_update.add_argument('-s', '--static', action=StaticChecker, nargs='*',
                            default=SUPPRESS, help=\
   'List of files and directories containing static '
   'content to be displayed by the deployed application')
    cmd_update.add_argument('-p', '--package', action=PackageChecker, nargs='+',
                            required=True,
                            help=\
    'List of paths to the package directories to be deployed. '
    'This argument is required')
    cmd_test = subparsers.add_parser('test', help=\
                        'Test the deployment in a stand-alone environment')
    cmd_test.add_argument('deploy', action=DeployChecker, help=\
                        'Defines the path to the deployment directory')
    cmd_upload = subparsers.add_parser('upload', help=\
                        'Upload the deployment to Google App Engine')
    cmd_upload.add_argument('deploy', action=DeployChecker, help=\
                        'Defines the path to the deployment directory')
    return parser.parse_args(args)                                                        

def createDeployment(config):
    d = config.deploy

def updateDeployment(config):
    pass

def testDeployment(config):
    pass

def uploadDeployment(config):
    pass

if __name__ == '__main__':
    main()