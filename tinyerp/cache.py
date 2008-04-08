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

import os
import re
import cPickle

import cherrypy
from turbogears.i18n import tg_gettext

import rpc

def memoize(limit=100, force=False):

    def memoize_wrapper(func):

        # Don't use cache for development environment
        if not force and cherrypy.config.get('server.environment') == 'development':
            return func

        queue = []
        store = {}

        def func_wrapper(*args, **kwargs):
            key = cPickle.dumps((args, kwargs))
            try:
                queue.append(queue.pop(queue.index(key)))
            except ValueError:
                store[key] = func(*args, **kwargs)
                queue.append(key)
                if limit is not None and len(queue) > limit:
                    del store[queue.pop(0)]

            return store[key]

        func_wrapper.func_name = func.func_name
        return func_wrapper

    return memoize_wrapper

@memoize(100)
def fields_view_get(model, view_id, view_type, context, hastoolbar=False):
    return rpc.RPCProxy(model).fields_view_get(view_id, view_type, context, hastoolbar)

@memoize(100)
def fields_get(model, fields, context):
    return rpc.RPCProxy(model).fields_get(fields, context)

@memoize(10000, True)
def _gettext(key, locale, domain):
    return tg_gettext.tg_gettext(key, locale, domain)

def gettext(key, locale=None, domain=None):

    if key in _MESSAGES:
        locale = locale or tg_gettext.get_locale()
        return _gettext(key, locale, domain)

    return key

def _load_translatables():

    result = []

    localedir = tg_gettext.get_locale_dir()
    po = os.path.join(localedir, 'fr', 'LC_MESSAGES', 'messages.po')

    pat = re.compile("""^msgid (.*?)^msgstr""", re.M+re.S)
    text = open(po).read()

    res = pat.search(text)
    while res:
        lines = res.group(1).split('\n')
        lines = [line.strip('"').replace('\\n', '') for line in lines if line]
        key = "\n".join(lines).strip()

        result.append(ustr(key))

        res = pat.search(text, res.end())

    return result

_MESSAGES = _load_translatables()

