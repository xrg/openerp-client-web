# -*- coding: UTF-8 -*-
"""This module contains functions called from console script entry points."""

import os
import sys

from os.path import exists

# ubuntu 8.04 has obsoleted `pyxml` package and installs here.
# the path needs to be updated before any `import xml`
_oldxml = '/usr/lib/python%s/site-packages/oldxml' % sys.version[:3]
if exists(_oldxml):
    sys.path.append(_oldxml)


import pkg_resources
pkg_resources.require("TurboGears")

import turbogears
import cherrypy

cherrypy.lowercase_api = True

class ConfigurationError(Exception):
    pass

def start(configfile=None):
    """Start the CherryPy application server."""

    if configfile is None:
        try:
            configfile = pkg_resources.resource_filename(
              pkg_resources.Requirement.parse("openerp-web"), 
                "config/default.cfg")
        except pkg_resources.DistributionNotFound:
            raise ConfigurationError(_("Could not find default configuration."))

    if not exists(configfile):
        raise ConfigurationError(_("Could not find configuration file: %s") % configfile)

    turbogears.update_config(configfile=configfile, modulename="openerp.config")
    
    # save the name of the configfile (TODO: config editor)
    import openerp
    openerp.CONFIG_FILE = configfile
    
    from openerp.controllers import Root

    turbogears.start_server(Root())
    
# vim: ts=4 sts=4 sw=4 si et

