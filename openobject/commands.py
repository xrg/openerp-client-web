import os
import sys
from optparse import OptionParser

import cherrypy
from cherrypy._cpconfig import as_dict

import openobject
import openobject.release

class ConfigurationError(Exception):
    pass

DISTRIBUTION_CONFIG = os.path.join('doc', 'openerp-web.cfg')
def get_config_file():
    setupdir = os.path.dirname(os.path.dirname(__file__))
    isdevdir = os.path.isfile(os.path.join(setupdir, 'setup.py'))
    configfile = '/etc/openerp-web.cfg'
    if isdevdir or not os.path.exists(configfile):
        configfile = os.path.join(setupdir, DISTRIBUTION_CONFIG)
    return configfile

def start():

    parser = OptionParser(version="%s" % (openobject.release.version))
    parser.add_option("-c", "--config", metavar="FILE", dest="config",
                      help="configuration file", default=get_config_file())
    parser.add_option("-a", "--address", help="host address, overrides server.socket_host")
    parser.add_option("-p", "--port", help="port number, overrides server.socket_port")
    parser.add_option("--no-static", dest="static",
                      action="store_false", default=True,
                      help="Disables serving static files through CherryPy")
    options, args = parser.parse_args(sys.argv)

    if not os.path.exists(options.config):
        raise ConfigurationError(_("Could not find configuration file: %s") %
                                 options.config)
                                 
    app_config = as_dict(options.config)
    
    openobject.configure(app_config)
    if options.static:
        openobject.enable_static_paths()
    
    if options.address:
        cherrypy.config['server.socket_host'] = options.address
    if options.port:
        try:
            cherrypy.config['server.socket_port'] = int(options.port)
        except:
            pass

    cherrypy.engine.start()
    cherrypy.engine.block()
