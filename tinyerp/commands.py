# -*- coding: UTF-8 -*-
"""This module contains functions called from console script entry points."""

import os
import sys

# ubuntu 8.04 has obsoleted `pyxml` package and installs here.
# the path needs to be updated before any `import xml`
_oldxml = '/usr/lib/python%s/site-packages/oldxml' % sys.version[:3]
if os.path.exists(_oldxml):
    sys.path.append(_oldxml)

from os.path import dirname, exists, join

import pkg_resources
pkg_resources.require("TurboGears")

import turbogears
import cherrypy

cherrypy.lowercase_api = True

class ConfigurationError(Exception):
    pass

def start():
    """Start the CherryPy application server."""

    setupdir = dirname(dirname(__file__))
    curdir = os.getcwd()

    # First look on the command line for a desired config file,
    # if it's not on the command line, then look for 'setup.py'
    # in the current directory. If there, load configuration
    # from a file called 'dev.cfg'. If it's not there, the project 
    # is probably installed and we'll look first for a file called
    # 'prod.cfg' in the current directory and then for a default
    # config file called 'default.cfg' packaged in the egg.
    if len(sys.argv) > 1:
        configfile = sys.argv[1]
    elif exists(join(setupdir, "setup.py")):
        configfile = join(setupdir, "dev.cfg")
    elif exists(join(curdir, "prod.cfg")):
        configfile = join(curdir, "prod.cfg")
    else:
        try:
            configfile = pkg_resources.resource_filename(
              pkg_resources.Requirement.parse("eTiny"), 
                "config/default.cfg")
        except pkg_resources.DistributionNotFound:
            raise ConfigurationError(_("Could not find default configuration."))

    turbogears.update_config(configfile=configfile,
        modulename="tinyerp.config")
    
    # save the name of the configfile (TODO: config editor)
    import tinyerp
    tinyerp.CONFIG_FILE = configfile
    
    from tinyerp.controllers import Root

    turbogears.start_server(Root())
    
# vim: ts=4 sts=4 sw=4 si et

