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
# -   All names, links and logos of Tiny, OpenERP and Axelor must be
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
import copy
import cPickle

import cherrypy

import rpc

__cache = {}

def clear():
    queue, store = __cache.setdefault(rpc.session.db, ([], {}))
    while queue:
        del store[queue.pop()]

def memoize(limit=100, force=False):

    def memoize_wrapper(func):

        # Don't use cache for development environment
        if not force and cherrypy.config.get('server.environment') == 'development':
            return func

        def func_wrapper(*args, **kwargs):

            queue, store = __cache.setdefault(rpc.session.db, ([], {}))

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
