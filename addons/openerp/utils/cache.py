###############################################################################
#
#  Copyright (C) 2007-TODAY OpenERP SA. All Rights Reserved.
#
#  $Id$
#
#  Developed by OpenERP (http://openerp.com) and Axelor (http://axelor.com).
#
#  The OpenERP web client is distributed under the "OpenERP Public License".
#  It's based on Mozilla Public License Version (MPL) 1.1 with following 
#  restrictions:
#
#  -   All names, links and logos of OpenERP must be kept as in original
#      distribution without any changes in all software screens, especially
#      in start-up page and the software header, even if the application
#      source code has been changed or updated or code has been added.
#
#  You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################
import copy
import cPickle
import functools

import cherrypy
from mako.util import LRUCache

import rpc

__cache = LRUCache(cherrypy.config.get('server.db_cache_size', 8))

def clear():
    __cache.pop(rpc.session.db, None)

def memoize(limit=100, force=False):

    def memoize_wrapper(func):

        # Don't use cache for development environment
        if not force and cherrypy.config.get('server.environment') == 'development':
            return func

        func_name = "%s.%s.%s" % (func.__module__, func.func_code.co_firstlineno, func.func_name)
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):

            store = __cache.setdefault(rpc.session.db, {}).setdefault(func_name, LRUCache(limit))

            key = cPickle.dumps((args, kwargs))
            if key not in store:
                store[key] = func(*args, **kwargs)
            return copy.deepcopy(store[key])

        return func_wrapper
    return memoize_wrapper

@memoize(1000)
def __fields_view_get(model, view_id, view_type, context, hastoolbar, hassubmenu, uid):
    return rpc.RPCProxy(model).fields_view_get(view_id, view_type, context, hastoolbar, hassubmenu)

def fields_view_get(model, view_id, view_type, context, hastoolbar=False, hassubmenu=False):
    return __fields_view_get(model, view_id, view_type, context, hastoolbar=hastoolbar, hassubmenu=hassubmenu, uid=rpc.session.uid)

@memoize(1000)
def __fields_get(model, fields, context, uid):
    return rpc.RPCProxy(model).fields_get(fields, context)

def fields_get(model, fields, context):
    return __fields_get(model, fields, context, uid=rpc.session.uid)

@memoize(1000)
def __can_write(model, uid):
    proxy = rpc.RPCProxy('ir.model.access')
    try:
        return proxy.check(model, 'write')
    except:
        pass
    return False

def can_write(model):
    return __can_write(model, uid=rpc.session.uid)

@memoize(1000)
def __can_read(model, uid):
    proxy = rpc.RPCProxy('ir.model.access')
    try:
        return proxy.check(model, 'read')
    except:
        pass
    return False

def can_read(model):
    return __can_read(model, uid=rpc.session.uid)

# vim: ts=4 sts=4 sw=4 si et
