'''
Created on 2011-03-01

@author: jonathan
'''
import unittest
from os.path import join, isdir, exists, isfile

from petaapan.utilities.deploygae import getConfig


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testVersion(self):
        print('\ntestVersion')
        self.DoExit(['--version'])
        
    def testHelp1(self):
        print('\ntest long help')
        self.DoExit(['--help'])
        
    def testHelp2(self):
        print('\ntest short help')
        self.DoExit(['-h'])
        
    def testNoArgs(self):
        print('\ntest no arguments')
        self.DoExit()
        
    def testHelpCreate(self):
        print('\ntest create help')
        self.DoExit(['create', '--help'])
                
    def testHelpUpdate(self):
        print('\ntest update help')
        self.DoExit(['update', '--help'])
        
    def testHelpTest(self):
        print('\ntest test help')
        self.DoExit(['test', '--help'])
        
    def testHelpUpload(self):
        print('\ntest upload help')
        self.DoExit(['upload', '--help'])
        
    def testSubcommandByItself(self):
        print('\ntest bare subcommand')
        self.DoExit(['create'])
        
    def testCreateNoStatic(self):
        args = []
        args.append('create')
        args.append('-p')
        args.append('.')
        args.append(join('..', '..', 'PublishSubscribeServer','src'))
        args.append(join('..', '..', 'PublishSubscribeClient', 'src'))
        args.append('--')
        args.append(join('..', '..', 'PublishSubscribeServer', 'deploy'))
        print('\ntest create with no static files: %s' % args)
        config = getConfig(args)
        self.assertTrue(config is not None)
        self.checkDeployExists(config, True)
        self.checkDirectories(config.package)
        
    def testCreateStatic1(self):
        args = []
        args.append('create')
        args.append('-p')
        args.append('.')
        args.append(join('..', '..', 'PublishSubscribeServer','src'))
        args.append(join('..', '..', 'PublishSubscribeClient', 'src'))
        args.append('--static')
        args.append(join('..', '..', 'Administration', 'home', 'WebContent',
                         'favicon.ico'))
        args.append('--')
        args.append(join('..', '..', 'PublishSubscribeServer', 'deploy'))
        print('\ntest create with static files: %s' % args)
        config = getConfig(args)
        self.assertTrue(config is not None)
        self.checkDeployExists(config, True)
        self.checkDirectories(config.package)
        self.checkFilesandDirectories(config.static)
        
    def testCreateStatic2(self):
        args = []
        args.append('create')
        args.append('--static')
        args.append(join('..', '..', 'Administration', 'home', 'WebContent',
                         'favicon.ico'))
        args.append('-p')
        args.append('.')
        args.append(join('..', '..', 'PublishSubscribeServer','src'))
        args.append(join('..', '..', 'PublishSubscribeClient', 'src'))
        args.append('--')
        args.append(join('..', '..', 'PublishSubscribeServer', 'deploy'))
        print('\ntest create with static files: %s' % args)
        config = getConfig(args)
        self.assertTrue(config is not None)
        self.checkDeployExists(config, True)
        self.checkDirectories(config.package)
        self.checkFilesandDirectories(config.static)

        
    def testUpdateNoStatic(self):
        args = []
        args.append('update')
        args.append('-p')
        args.append('.')
        args.append(join('..', '..', 'PublishSubscribeServer','src'))
        args.append(join('..', '..', 'PublishSubscribeClient', 'src'))
        args.append('--')
        args.append(join('..', '..', 'PublishSubscribeServer', 'deploy'))
        print('\ntest update with no static files: %s' % args)
        config = getConfig(args)
        self.assertTrue(config is not None)
        self.checkDeployExists(config, True)
        self.checkDirectories(config.package)
        
    def testUpdateStatic1(self):
        args = []
        args.append('update')
        args.append('-p')
        args.append('.')
        args.append(join('..', '..', 'PublishSubscribeServer','src'))
        args.append(join('..', '..', 'PublishSubscribeClient', 'src'))
        args.append('--static')
        args.append(join('..', '..', 'Administration', 'home', 'WebContent',
                         'favicon.ico'))
        args.append('--')
        args.append(join('..', '..', 'PublishSubscribeServer', 'deploy'))
        print('\ntest update with static files: %s' % args)
        config = getConfig(args)
        self.assertTrue(config is not None)
        self.checkDeployExists(config, True)
        self.checkDirectories(config.package)
        self.checkFilesandDirectories(config.static)
        
    def testUpdateStatic2(self):
        args = []
        args.append('update')
        args.append('--static')
        args.append(join('..', '..', 'Administration', 'home', 'WebContent',
                         'favicon.ico'))
        args.append('-p')
        args.append('.')
        args.append(join('..', '..', 'PublishSubscribeServer','src'))
        args.append(join('..', '..', 'PublishSubscribeClient', 'src'))
        args.append('--')
        args.append(join('..', '..', 'PublishSubscribeServer', 'deploy'))
        print('\ntest update with static files: %s' % args)
        config = getConfig(args)
        self.assertTrue(config is not None)
        self.checkDeployExists(config, True)
        self.checkDirectories(config.package)
        self.checkFilesandDirectories(config.static)
        
    def checkDeployExists(self, config, create):
        '''
        Helper for tests that need to test for the existence of a
        deployment directory
        '''
#        args = join('..', '..', '..', '..', '..',
#                    'PublishSubscribeServer', 'deploy')
#        config = getConfig([args])
        deploy = config.deploy
        self.assertNotEqual(deploy, None)
        self.assertTrue(deploy[0])
        self.assertTrue(isdir(deploy[1]) or (create and not deploy[0]))
        
    def checkFilesandDirectories(self, l):
        '''
        Helper that verifies that an argument contains a list
        of files and directories that exist
        '''
        self.assertNotEqual(l, None)
        self.assertNotEqual(len(l), 0)
        for e in l:
            self.assertTrue(isdir(e) or isfile(e))
        
    def checkDirectories(self, l):
        '''
        Helper that verifies that an argument contains a list
        of directories that exist
        '''
        self.assertNotEqual(l, None)
        self.assertNotEqual(len(l), 0)
        for e in l:
            self.assertTrue(isdir(e))
                
        
    def DoExit(self, args=None):
        '''Helper for tests that are expected to throw a SystemExit exception'''
        
        try:
            getConfig(args)
            self.fail('The test should have raised a System Exit exception')
        except SystemExit:
            pass # This is what was expected
        except BaseException, ex:
            self.fail('Unexpected exception %s' % (str(ex)))
            raise ex


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()