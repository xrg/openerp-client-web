###############################################################################
#
# Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
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
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
###############################################################################

import cPickle
import rpc

def memoize(function, limit=None):
    if isinstance(function, int):
        def memoize_wrapper(f):
            return memoize(f, function)

        return memoize_wrapper

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

    @memoize(500)
    def get_view(self, model, view_id, view_type, context, hastoolbar=False):
        return rpc.RPCProxy(model).fields_view_get(view_id, view_type, context, hastoolbar)

cache = CacheManager()
