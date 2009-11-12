
import os
import sys
import imp

import cherrypy


ADDONS_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ADDONS_PATH)


def imp_module(name):
    fp, pathname, description = imp.find_module(name, [ADDONS_PATH])
    try:
        return imp.load_module(name, fp, pathname, description)
    finally:
        if fp:
            fp.close()
            

def load_addons(config):
    
    addons = [f for f in os.listdir(ADDONS_PATH) \
              if os.path.isfile(os.path.join(ADDONS_PATH, f, "__terp__.py"))]
              
    
    sys.modules.pop("openerp.addons", None)
    
    for name in addons:
        
        cherrypy.log("Loading module '%s'" % name, "INFO")
        
        m = imp_module(name)
                
        static = os.path.join(ADDONS_PATH, name, "static")
        if os.path.isdir(static):
            base = imp_module("base")
            base.widgets.register_resource_directory(config, name, static)

