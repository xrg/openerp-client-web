###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# The OpenERP web client is distributed under the "OpenERP Public License".
# It's based on Mozilla Public License Version (MPL) 1.1 with following
# restrictions:
#
# -   All names, links and logos of Tiny, Open ERP and Axelor must be
#     kept as in original distribution without any changes in all software
#     screens, especially in start-up page and the software header, even if
#     the application source code has been changed or updated or code has been
#     added.
#
# -   All distributions of the software must keep source code with OEPL.
#
# -   All integrations to any other software must keep source code with OEPL.
#
# If you need commercial licence to remove this kind of restriction please
# contact us.
#
# You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################

"""
This modules implements custom authorization logic for the OpenERP Web Client.
"""

import types
import cherrypy

from utils import secured


__all__ = ["BaseController", "SecuredController", "mount_tree"]

_REGISTRY = {}

def mount_tree(mount, config):
    
    root = _REGISTRY.get("/", None)
    
    if not root:
        raise Exception("There is no root controller.")
    
    cherrypy.log("Registering controller '%s'" % "/", "INFO")
    
    keys = _REGISTRY.keys()
    keys.sort()
    
    for p in keys:
        
        if p == "/":
            continue
        
        paths = p.split("/")
        
        last = paths[-1]
        rest = "/".join(paths[:-1]) or "/"
                
        parent = _REGISTRY.get(rest)
        if not parent:
            raise Exception("Unable to mount '%s', no parent." % p)
                
        cherrypy.log("Registering controller '%s'" % p, "INFO")
        
        c = _REGISTRY[p]
        parent._subcontrollers[last] = c()
        
    return cherrypy.tree.mount(root(), mount, config)
    

class ControllerType(type):
    
    def __new__(cls, name, bases, attrs):
        
        obj = super(ControllerType, cls).__new__(cls, name, bases, attrs)    
        path = attrs.get("_cp_path")
        
        if "path" in attrs and name != "BaseController":
            raise Exception("Can't override 'path' attribute.")
        
        if path == "/" and path in _REGISTRY:        
            raise Exception("There should be only one root controller.")
        
        if path in _REGISTRY:
            raise Exception("'%s' is already registered." % (path))
        
        if path:
            if not path.startswith("/"):
                raise Exception("Invalid path '%s', should start with '/'." % (path))
            
            _REGISTRY[path] = obj
        
        return obj


class BaseController(object):
    
    __metaclass__ = ControllerType
    
    _cp_path = None
    
    _subcontrollers = {}
    
    def __new__(cls):
        o = super(BaseController, cls).__new__(cls)
        for n, c in o._subcontrollers.items():
            setattr(o, n, c)
        return o
    
    def _get_path(self):
        return self._cp_path
    
    path = property(_get_path)
    
class SecuredController(BaseController):

    def __getattribute__( self, name ):
        value= object.__getattribute__(self, name)

        if isinstance(value, types.MethodType ) and hasattr(value, "exposed") and not (hasattr(value, "secured") and not value.secured):
            return secured(value)

        # Some other property
        return value


# vim: ts=4 sts=4 sw=4 si et

