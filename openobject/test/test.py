import os
import sys

from openobject import commands

from cherrypy.test import test, helper
test.prefer_parent_path()

import cherrypy

__all__ = ["TestCase", "setup_server"]

class TestCase(helper.CPWebCase):
    pass

commands.CPSessionWrapper = dict

class CPSessionWrapper(dict):
    
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        return self.get(name)

    def __delattr__(self, name):
        if name in self:
            del self[name]

commands.CPSessionWrapper = CPSessionWrapper

def setup_server():
    configfile = commands.get_config_file()
    commands.setup_server(configfile)
    cherrypy.config.update({'environment': 'test_suite'})

def run():
    
    testList = [
        'test_root_controller',
    ]
    
    clp = test.CommandLineParser(testList)
    success = clp.run()
    if clp.interactive:
        print
        raw_input('hit enter')
    sys.exit(success)


if __name__ == '__main__':
    run()
