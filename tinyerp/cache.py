###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the 
# Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
# Boston, MA  02111-1307, USA.
#
###############################################################################

import cPickle
import rpc
import cherrypy

def memoize(function, limit=None):

    if isinstance(function, int):
        def memoize_wrapper(f):
            return memoize(f, function)

        return memoize_wrapper
    
    # Don't use cache for development environment
    if cherrypy.config.get('server.environment') == 'development':
        return function

    store = {}
    queue = []

    def memoize_wrapper(*args, **kwargs):
        key = cPickle.dumps((args, kwargs))
        try:
            queue.append(queue.pop(queue.index(key)))
        except ValueError:
            store[key] = function(*args, **kwargs)
            queue.append(key)
            if limit is not None and len(queue) > limit:
                del store[queue.pop(0)]

        return store[key]

    memoize_wrapper.func_name = function.func_name

    return memoize_wrapper

class CacheManager(object):
    
    @memoize(100)
    def fields_view_get(self, model, view_id, view_type, context, hastoolbar=False):
        return rpc.RPCProxy(model).fields_view_get(view_id, view_type, context, hastoolbar)

    @memoize(100)
    def fields_get(self, model, fields, context):
        return rpc.RPCProxy(model).fields_get(fields, context)

cache = CacheManager()
