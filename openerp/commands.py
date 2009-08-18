# -*- coding: UTF-8 -*-
"""This module contains functions called from console script entry points."""

import os
import sys
import optparse

from os.path import join, dirname, exists

import cherrypy
from cherrypy._cpconfig import as_dict
from formencode import NestedVariables

from openerp import release


__all__ = ['start']


def nestedvars_tool():
    if hasattr(cherrypy.request, 'params'):
        cherrypy.request.params = NestedVariables.to_python(cherrypy.request.params or {})

cherrypy.tools.nestedvars = cherrypy.Tool("before_handler", nestedvars_tool)
cherrypy.lowercase_api = True


class CPSessionWrapper(object):

    def __setattr__(self, name, value):
        cherrypy.session[name] = value

    def __getattr__(self, name):
        return cherrypy.session.get(name)

    def __delattr__(self, name):
        if name in cherrypy.session:
            del cherrypy.session[name]

    __getitem__ = __getattr__
    __setitem__ = __setattr__

    def get(self, name, default=None):
        return cherrypy.session.get(name, default)

    def clear(self):
        cherrypy.session.clear()


class ConfigurationError(Exception):
    pass


def get_config_file():
    setupdir = dirname(dirname(__file__))
    configfile = join(setupdir, "config", "openerp-web.cfg")
    if exists(configfile):
        return configfile
    return None


def setup_server(configfile):

    if not exists(configfile):
        raise ConfigurationError(_("Could not find configuration file: %s") % configfile)


    cherrypy.config.update({
        'tools.sessions.on':  True,
        'tools.nestedvars.on':  True
    })

    app_config = as_dict(configfile)
    
    _global = app_config.pop('global', {})
    _environ = _global.setdefault('server.environment', 'development')
    
    if _environ != 'development':
        _global['environment'] = _environ
        
    cherrypy.config.update(_global)
    
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app_config.update({'/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': static_dir
    }})
    
    app_config.update({'/favicon.ico': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': static_dir + "/images/favicon.ico"
    }})

    app_config.update({'/LICENSE.txt': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': static_dir + "/../../doc/LICENSE.txt"
    }})

    # import profiler while makes profile decorator available as __builtins__
    from openerp import profiler
    
    from openerp.controllers.root import Root
    app = cherrypy.tree.mount(Root(), '/', app_config)

    import pkg_resources
    from openerp.widgets import register_resource_directory

    static = pkg_resources.resource_filename("openerp", "static")
    register_resource_directory(app, "openerp", static)

    # initialize the rpc session
    host = app.config['openerp'].get('host')
    port = app.config['openerp'].get('port')
    protocol = app.config['openerp'].get('protocol')

    from openerp import rpc
    rpc.initialize(host, port, protocol, storage=CPSessionWrapper())


def start():
    """Start the CherryPy application server."""

    parser = optparse.OptionParser(version=release.version)
    parser.add_option("-c", "--config", dest="config", help="specify alternate config file", default=get_config_file())
    (opt, args) = parser.parse_args()

    setup_server(opt.config)

    cherrypy.engine.start()
    cherrypy.engine.block()



# vim: ts=4 sts=4 sw=4 si et

