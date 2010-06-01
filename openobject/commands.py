import os
import sys
from optparse import OptionParser

import cherrypy
from cherrypy._cpconfig import as_dict

import openobject
import openobject.release

class ConfigurationError(Exception):
    pass

def get_config_file():
    setupdir = os.path.dirname(os.path.dirname(__file__))
    configfile = os.path.join(setupdir, "config", "openobject-web.cfg")
    if os.path.exists(configfile):
        return configfile
    return None

def start():

    parser = OptionParser(version="%s" % (openobject.release.version))
    parser.add_option("-c", "--config", metavar="FILE", dest="config",
                      help="configuration file", default=get_config_file())
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

    cherrypy.engine.start()
    cherrypy.engine.block()
