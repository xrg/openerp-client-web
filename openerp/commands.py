import os
import sys
from optparse import OptionParser

import cherrypy
from cherrypy._cpconfig import as_dict

from openerp import release
      
           
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
    setupdir = os.path.dirname(os.path.dirname(__file__))
    configfile = os.path.join(setupdir, "config", "openerp-web.cfg")
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

    # import profiler while makes profile decorator available as __builtins__
    from openerp.tools import profiler
    from openerp.addons import load_addons
    
    load_addons(app_config)
    
    from base.controllers import mount_tree
    mount = cherrypy.config.get('server.webpath', '/')
    app = mount_tree(mount, app_config)

    # initialize the rpc session
    host = app.config['openerp'].get('host')
    port = app.config['openerp'].get('port')
    protocol = app.config['openerp'].get('protocol')

    from openerp.tools import rpc
    rpc.initialize(host, port, protocol, storage=CPSessionWrapper())
    
   
def start():
    
    parser = OptionParser(version="%s" % (release.version))
    parser.add_option("-c", "--config", metavar="FILE", dest="config", help="configuration file", default=get_config_file())
    options, args = parser.parse_args(sys.argv)
    
    setup_server(options.config)
    
    cherrypy.engine.start()
    cherrypy.engine.block()

