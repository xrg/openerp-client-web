#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Start script for the openerp-web TurboGears project.

This script is only needed during development for running from the project 
directory. When the project is installed, easy_install will create a
proper start script.
"""

import os
import sys
import optparse
from os.path import join, dirname, exists
from openerp.commands import start, ConfigurationError
from openerp.release import version

def get_config_file():
    configfile = None
    setupdir = dirname(dirname(__file__))
    curdir = os.getcwd()
    if exists(join(setupdir, "setup.py")):
        configfile = join(setupdir, "dev.cfg")
    elif exists(join(curdir, "prod.cfg")):
        configfile = join(curdir, "prod.cfg")
    return configfile

if __name__ == "__main__":
    try:
        # First look on the command line for a desired config file,
        # if it's not on the command line, then look for 'setup.py'
        # in the current directory. If there, load configuration
        # from a file called 'dev.cfg'. If it's not there, the project 
        # is probably installed and we'll look first for a file called
        # 'prod.cfg' in the current directory and then for a default
        # config file called 'default.cfg' packaged in the egg.
        parser = optparse.OptionParser(version=version)
        parser.add_option("-c", "--config", dest="config", help="specify alternate config file",
                          default=get_config_file())
        (opt, args) = parser.parse_args()

        start(opt.config)
    except ConfigurationError, exc:
        sys.stderr.write(str(exc)+"\n")
        sys.exit(1)

# vim: ts=4 sts=4 sw=4 si et

