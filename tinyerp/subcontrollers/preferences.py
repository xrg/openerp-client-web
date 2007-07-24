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

import re
import time

from turbogears import expose
from turbogears import controllers
from turbogears import redirect

import cherrypy

from tinyerp import rpc
from tinyerp.tinyres import TinyResource
from tinyerp.utils import TinyDict

from tinyerp.widgets.screen import Screen

class Preferences(controllers.Controller, TinyResource):

    @expose(template="tinyerp.subcontrollers.templates.preferences")
    def create(self):
        proxy = rpc.RPCProxy('ir.values')

        res = proxy.get('meta', False, [('res.users', rpc.session.uid)], False, rpc.session.context, True, True, False)

        values = {}
        defaults = {}
        for (n, k, v) in res:
            values[k] = v
            defaults[k] = n

        id = rpc.session.uid
        model = 'res.users'
        preferences = proxy.get('meta', False, [('res.users', False)], True, rpc.session.context, True)

        fields = {}
        arch = '<?xml version="1.0"?><form string="%s">\n' % ('Preferences')
        for p in preferences:
            arch+='<field name="%s" colspan="4"/>' % (p[1],)
            fields[p[1]] = p[3]
        arch+= '</form>'

        params = TinyDict()

        params.model = model
        params.context = {}
        params.domain = []

        view = dict(arch=arch, fields=fields, datas=values)

        screen = Screen(params, editable=True)
        screen.add_view(view)

        return dict(screen=screen, defaults=defaults)

    @expose()
    def ok(self, **kw):
        params, data = TinyDict.split(kw)
        for key in data:
            if data[key]:
                rpc.session.execute('object', 'execute', 'ir.values', 'set', 'meta', key, key, [(params.model, rpc.session.uid)], data[key])
            elif params.default.get(key, False):
                res = rpc.session.execute('common', 'ir_del', params.default[key])

        rpc.session.context_reload()
        raise redirect('/')
