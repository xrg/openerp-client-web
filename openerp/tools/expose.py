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

import cherrypy
import simplejson

from mako.template import Template
from mako.lookup import TemplateLookup


__all__ = ['find_resource', 'load_template', 'expose']


def find_resource(package_or_module, *names):

    ref = package_or_module
    if isinstance(package_or_module, basestring):
        ref = __import__(package_or_module, globals(), \
                fromlist=package_or_module.split('.'))

    return os.path.abspath(os.path.join(os.path.dirname(ref.__file__), *names))


def load_template(template, module=None):

    if not template:
        return template
    
    if module:
        template = find_resource(module, template)
    else:
        template = os.path.abspath(template)
        
    dirname = os.path.dirname(template)
    template = os.path.basename(template)
    
    #lookup = TemplateLookup(directories=[dirname], module_directory=dirname)
    lookup = TemplateLookup(directories=[dirname])
    return lookup.get_template(template)


def expose(format='html', template=None, content_type='text/html', allow_json=False):

    if format == 'json':
        content_type = 'text/javascript'

    def expose_wrapper(func):

        def func_wrapper(*args, **kw):
            
            tmpl = load_template(template, func.__module__)
            res = func(*args, **kw)

            cherrypy.response.headers['content-type'] = content_type

            if format == 'json' or (allow_json and 'allow_json' in cherrypy.requests.params):
                return simplejson.dumps(res)

            if tmpl:
                res = tmpl.render(**res)

            return str(res)

        func_wrapper.func_name = func.func_name
        func_wrapper.exposed = True

        return func_wrapper

    return expose_wrapper


# vim: ts=4 sts=4 sw=4 si et
