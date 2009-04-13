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

import os
import re
import types

import cherrypy
import simplejson

from mako.template import Template
from mako.lookup import TemplateLookup

from openerp.tools import utils

__all__ = ['find_resource', 'load_template', 'renderer', 'expose']


def find_resource(package_or_module, *names):

    ref = package_or_module
    if isinstance(package_or_module, basestring):
        ref = __import__(package_or_module, globals(), \
                fromlist=package_or_module.split('.'))

    return os.path.abspath(os.path.join(os.path.dirname(ref.__file__), *names))


#TODO: @cache.memoize(1000)
def load_template(template, module=None):

    if not template:
        return template
        
    if re.match('(.+)\.(html|mako)\s*$', template):
        
        if module:
            template = find_resource(module, template)
        else:
            template = os.path.abspath(template)

        dirname = os.path.dirname(template)
        basename = os.path.basename(template)
    
        #lookup = TemplateLookup(directories=[dirname], module_directory=dirname)
        lookup = TemplateLookup(directories=[dirname])
        return lookup.get_template(basename)
        
    else:
        return Template(template)
    
    
def _config(key, section, default=None):
    return cherrypy.request.app.config.get(section, {}).get(key, default)

class _Provider(dict):
    
    def __getattr__(self, name):
        if name in self:
            return self[name]
        return super(Bunch, self).__getattribute__(name)
    
    def __setattr__(self, name, value):
        raise AttributeError

_var_providers = {}

def register_template_vars(callback, prefix='oo'):
    providers = _var_providers.setdefault(prefix, [])
    providers.append(callback)
    
def _cp_vars():
    
    return {
        'session': cherrypy.session,
        'request': cherrypy.request,
        'config': _config,
    }
    
def _py_vars():
    
    return {
        'url': utils.url,
        'attrs': utils.attrs,
        'attr_if': utils.attr_if,
        'checker': lambda e: utils.attr_if('checked', e),
        'selector': lambda e: utils.attr_if('selected', e),        
        'readonly': lambda e: utils.attr_if('readonly', e),
        'disabled': lambda e: utils.attr_if('disabled', e),
    }
    
def _root_vars():
    return {
        'rpc': rpc,
    }
    
register_template_vars(_cp_vars, 'cp')
register_template_vars(_py_vars, 'py')
register_template_vars(_root_vars, None)


def renderer(template, module=None):
    
    tmpl = load_template(template, module)
    
    def wrapper(**kw):
        
        if not tmpl:
            return
        
        _vars = {}
        for prefix, cbs in _var_providers.iteritems():
            if prefix:
                provider = _Provider()
                for cb in cbs:
                    provider.update(cb())
                _vars[prefix] = provider
            else:
                _vars.update(cb())
        
        kw = kw.copy()
        kw.update(_vars)
        
        #TODO: encoding utf-8
        return tmpl.render(**kw)
    
    return wrapper

   
def expose(format='html', template=None, content_type='text/html', allow_json=False):

    def expose_wrapper(func):

        def func_wrapper(*args, **kw):
            
            res = func(*args, **kw)
            
            if format == 'json' or (allow_json and 'allow_json' in cherrypy.requests.params):
                cherrypy.response.headers['content-type'] = 'text/javascript'
                return simplejson.dumps(res)
            
            cherrypy.response.headers['content-type'] = content_type
            
            template = kw.get('cp_template') or template
            
            if template:
                
                from openerp.widgets.resource import merge_resources
                
                res['widget_resources'] = _resources = {}
                for k, w in res.iteritems():
                    if hasattr(w, 'retrieve_resources') and w.is_root:
                        _resources = merge_resources(_resources, w.retrieve_resources())

                return renderer(template, func.__module__)(**res)
            
            return unicode(res, 'utf-8')

        func_wrapper.func_name = func.func_name
        func_wrapper.exposed = True

        return func_wrapper

    return expose_wrapper


# vim: ts=4 sts=4 sw=4 si et

