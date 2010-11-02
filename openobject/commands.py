import os
import sys
from optparse import OptionParser

import babel.localedata

import cherrypy
from cherrypy._cpconfig import as_dict

import openobject
import openobject.release
import openobject.paths

class ConfigurationError(Exception):
    pass

DISTRIBUTION_CONFIG = os.path.join('doc', 'openerp-web.cfg')
def get_config_file():
    if hasattr(sys, 'frozen'):
        configfile = os.path.join(openobject.paths.root(), DISTRIBUTION_CONFIG)
    else:
        setupdir = os.path.dirname(os.path.dirname(__file__))
        isdevdir = os.path.isfile(os.path.join(setupdir, 'setup.py'))
        configfile = '/etc/openerp-web.cfg'
        if isdevdir or not os.path.exists(configfile):
            configfile = os.path.join(setupdir, DISTRIBUTION_CONFIG)
    return configfile

def configure_babel():
    """ If we are in a py2exe bundle, rather than babel being installed in
    a site-packages directory in an unzipped form with all its meta- and
    package- data it is split between the code files within py2exe's archive
    file and the metadata being stored at the toplevel of the py2exe
    distribution.
    """
    if not hasattr(sys, 'frozen'): return

    # the locale-specific data files are in babel/localedata/*.dat, babel
    # finds these data files via the babel.localedata._dirname filesystem
    # path.
    babel.localedata._dirname = openobject.paths.root('babel', 'localedata')

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

    configure_babel()

    cherrypy.engine.start()
    cherrypy.engine.block()
