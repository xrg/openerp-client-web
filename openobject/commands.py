import os
import sys
from optparse import OptionParser

import cherrypy
from cherrypy._cpconfig import as_dict

from openobject import release


class ConfigurationError(Exception):
    pass


def get_config_file():
    setupdir = os.path.dirname(os.path.dirname(__file__))
    configfile = os.path.join(setupdir, "config", "openobject-web.cfg")
    if os.path.exists(configfile):
        return configfile
    return None
            

def setup_server(configfile):

    if not os.path.exists(configfile):
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
    
    from openobject.dispatch import PooledDispatcher
    from openobject.tools import _tools
    
    app_config['/'] = {'request.dispatch': PooledDispatcher()}
    cherrypy.tree.mount(root=None, config=app_config)


def start():
    
    parser = OptionParser(version="%s" % (release.version))
    parser.add_option("-c", "--config", metavar="FILE", dest="config", help="configuration file", default=get_config_file())
    options, args = parser.parse_args(sys.argv)
    
    setup_server(options.config)
    
    cherrypy.engine.start()
    cherrypy.engine.block()

