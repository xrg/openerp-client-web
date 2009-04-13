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
import copy
import cPickle

import cherrypy

from gettext import translation

import rpc

__cache_references = []

def clear():
    for queue, store in __cache_references:
        while queue:
            del store[queue.pop()]

def memoize(limit=100, force=False):

    def memoize_wrapper(func):

        # Don't use cache for development environment
        if not force and cherrypy.config.get('server.environment') == 'development':
            return func

        queue = []
        store = {}
        
        __cache_references.append((queue, store))

        def func_wrapper(*args, **kwargs):
            key = cPickle.dumps((args, kwargs))
            try:
                queue.append(queue.pop(queue.index(key)))
            except ValueError:
                store[key] = func(*args, **kwargs)
                queue.append(key)
                if limit is not None and len(queue) > limit:
                    del store[queue.pop(0)]

            return copy.deepcopy(store[key])

        func_wrapper.func_name = func.func_name
        return func_wrapper

    return memoize_wrapper

@memoize(1000)
def __fields_view_get(model, view_id, view_type, context, hastoolbar, sid):
    return rpc.RPCProxy(model).fields_view_get(view_id, view_type, context, hastoolbar)

def fields_view_get(model, view_id, view_type, context, hastoolbar=False):
    return __fields_view_get(model, view_id, view_type, context, hastoolbar=hastoolbar, sid=cherrypy.session.id)

@memoize(1000)
def __fields_get(model, fields, context, sid):
    return rpc.RPCProxy(model).fields_get(fields, context)

def fields_get(model, fields, context):
    return __fields_get(model, fields, context, sid=cherrypy.session.id)

@memoize(1000)
def __can_write(model, sid):
    proxy = rpc.RPCProxy('ir.model.access')
    try:
        return proxy.check(model, 'write')
    except:
        pass
    return False

def can_write(model):
    return __can_write(model, sid=cherrypy.session.id)

@memoize(10000, True)
def _gettext(key, locale, domain):
    return tg_gettext.tg_gettext(key, locale, domain)

def gettext(key, locale=None, domain=None):
    if key in __TRANSLATABLES:
        return _gettext(key, locale or tg_gettext.get_locale(), 'messages')
    return key

def __load_translatables():

    localedir = tg_gettext.get_locale_dir()

    #XXX: TG bug #1631
    if not localedir:
        from turbogears import config
        config.update({'package': 'openerp'})
        localedir = tg_gettext.get_locale_dir()
    
    result = {}
    for lang in os.listdir(localedir):
        try:
            t = translation(domain='messages', localedir=localedir, languages=[lang])
            result.update(t._catalog)
        except:
            pass

    return result.keys()

#TODO: __TRANSLATABLES = __load_translatables()

# vim: ts=4 sts=4 sw=4 si et

