from os.path import join
from os import listdir, getcwd
from pprint import pprint
__path__.append(join(__path__[0],'..','..','..',
                     'PublishSubscribeClient', 'src','petaapan'))
__path__.append(join(__path__[0],'..','..','..',
                     'PublishSubscribeServer', 'src','petaapan'))
pprint('__PATH__')
pprint(__path__)
