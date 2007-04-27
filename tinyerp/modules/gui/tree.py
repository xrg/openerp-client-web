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

"""
This module implementes heirarchical tree view for a tiny model having
    view_type = 'tree'

@todo: Implemente tree view
"""

import xml.dom.minidom
import parser

from turbogears import expose
from turbogears import widgets
from turbogears import controllers

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp.tinyres import TinyResource
from tinyerp.widgets import tree_view

class Tree(controllers.Controller, TinyResource):

    @expose(template="tinyerp.modules.gui.templates.tree")
    def create(self, params):

        view_id = (params.view_ids or False) and params.view_ids[0]
        domain = params.domain
        context = params.context

        res_id = params.ids
        model = params.model

        if view_id:
            view_base =  rpc.session.execute('/object', 'execute', 'ir.ui.view', 'read', [view_id], ['model', 'type'], context)[0]
            model = view_base['model']
            proxy = rpc.RPCProxy(model)
            view = proxy.fields_view_get(view_id, view_base['type'], context)
        else:
            proxy = rpc.RPCProxy(model)
            view = proxy.fields_view_get(False, 'tree', context)

        tree = tree_view.ViewTree(view, model, res_id, domain=domain, context=context)

        return dict(tree=tree)

    @expose('json')
    def data(self, ids, model, fields, domain=[]):

        if isinstance(ids, basestring):
            ids = eval(ids)

        if isinstance(fields, basestring):
            fields = eval(fields)

        if isinstance(domain, basestring):
            domain = eval(domain)

        if 'child_ids' not in fields:
            fields.append('child_ids')

        proxy = rpc.RPCProxy(model)

        if ids == -1:
            ids = proxy.search(domain)

        ctx = {}
        ctx.update(rpc.session.context.copy())

        result = proxy.read(ids, fields, ctx)

        records = []
        for item in result:
            record = {}

            record['id'] = item.pop('id')
            record['children'] = []
            if 'child_ids' in item:
                record['children'] = item.pop('child_ids')

            record['data'] = item

            records += [record]

        return dict(records=records)
