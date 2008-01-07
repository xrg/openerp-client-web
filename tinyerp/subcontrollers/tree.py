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
"""

import time
import xml.dom.minidom

from turbogears import expose
from turbogears import widgets
from turbogears import controllers

from tinyerp import rpc
from tinyerp import icons
from tinyerp import tools
from tinyerp import common
from tinyerp.cache import cache

from tinyerp.tinyres import TinyResource
from tinyerp.widgets import tree_view

from tinyerp.utils import TinyDict

DT_FORMAT = '%Y-%m-%d'
DHM_FORMAT = '%Y-%m-%d %H:%M:%S'

class Tree(controllers.Controller, TinyResource):

    @expose(template="tinyerp.subcontrollers.templates.tree")
    def create(self, params):

        view_id = (params.view_ids or False) and params.view_ids[0]
        domain = params.domain
        context = params.context

        res_id = params.ids
        model = params.model

        if view_id:
            view_base =  rpc.session.execute('object', 'execute', 'ir.ui.view', 'read', [view_id], ['model', 'type'], context)[0]
            model = view_base['model']
            view = cache.fields_view_get(model, view_id, view_base['type'], context)
        else:
            view = cache.fields_view_get(model, False, 'tree', context)

        tree = tree_view.ViewTree(view, model, res_id, domain=domain, context=context, action="/tree/action")
        if tree.toolbar:
            for tool in tree.toolbar:
                tool['icon'] = icons.get_icon(tool['icon'])

        return dict(tree=tree)

    @expose()
    def default(self, id, model, domain):
        params = TinyDict()

        params.ids = id
        params.view_ids = [1]
        params.model = model
        params.domain = domain
        params.context = {}

        return self.create(params)

    def sort_callback(self, item1, item2, field, sort_order="asc"):
        a = item1[field]
        b = item2[field]

        if(sort_order == "dsc"):
            return -cmp(a, b)

        return cmp(a, b)

    @expose('json')
    def data(self, ids, model, fields, field_parent=None, icon_name=None, domain=[], context={}, sort_by=None, sort_order="asc"):

        ids = ids.split(',')
        ids = [int(id) for id in ids if id != '']

        if isinstance(fields, basestring):
            fields = fields.split(',')

        if isinstance(domain, basestring):
            domain = eval(domain)
            
        if isinstance(context, basestring):
            context = eval(context)

        if field_parent and field_parent not in fields:
            fields.append(field_parent)

        proxy = rpc.RPCProxy(model)
        
        ctx = context or {}
        ctx.update(rpc.session.context.copy())

        if icon_name:
            fields.append(icon_name)

        fields_info = cache.fields_get(model, fields, ctx)
        result = proxy.read(ids, fields, ctx)

        if sort_by:
            result.sort(lambda a,b: self.sort_callback(a, b, sort_by, sort_order))

        # formate the data
        for field in fields:

            if fields_info[field]['type'] in ('float', 'integer'):
                for x in result:
                    if x[field]:
                        x[field] = '%s'%(x[field])

            if fields_info[field]['type'] in ('date',):
                for x in result:
                    if x[field]:
                        date = time.strptime(x[field], DT_FORMAT)
                        x[field] = time.strftime('%x', date)

            if fields_info[field]['type'] in ('datetime',):
                for x in result:
                    if x[field]:
                        date = time.strptime(x[field], DHM_FORMAT)
                        x[field] = time.strftime('%x %H:%M:%S', date)

            if fields_info[field]['type'] in ('one2one', 'many2one'):
                for x in result:
                    if x[field]:
                        x[field] = x[field][1]

            if fields_info[field]['type'] in ('selection'):
                for x in result:
                    if x[field]:
                        x[field] = dict(fields_info[field]['selection']).get(x[field], '')

        records = []
        for item in result:

            # empty string instead of bool and None
            for k, v in item.items():
                if v==None or (v==False and type(v)==bool):
                    item[k] = ''

            record = {}

            record['id'] = item.pop('id')
            record['action'] = '/tree/open?model=%s&id=%s'%(model, record['id'])
            record['target'] = None

            record['icon'] = None

            if icon_name and icon_name in item:
                icon = item.pop(icon_name)
                record['icon'] = icons.get_icon(icon)

                if icon == 'STOCK_OPEN':
                    record['action'] = None

            record['children'] = []

            if field_parent and field_parent in item:
                record['children'] = item.pop(field_parent) or None

            record['data'] = item

            records += [record]

        return dict(records=records)

    def do_action(self, name, adds={}, datas={}):
        params, data = TinyDict.split(datas)

        model = params.model

        ids = data.get('ids') or []

        if ids:
            ids = [int(id) for id in ids.split(',')]

        id = (ids or False) and ids[0]

        if len(ids):
            from tinyerp.subcontrollers import actions
            return actions.execute_by_keyword(name, adds=adds, model=model, id=id, ids=ids, report_type='pdf')
        else:
            raise common.message(_("No record selected !"))

    @expose()
    def report(self, **kw):
        return self.do_action('client_print_multi', datas=kw)

    @expose()
    def action(self, **kw):
        return self.do_action('tree_but_action', datas=kw)

    @expose()
    def switch(self, **kw):

        params, data = TinyDict.split(kw)

        ids = data.get('ids') or []
        if ids:
            ids = [int(id) for id in ids.split(',')]

        if len(ids):
            from tinyerp.subcontrollers import actions
            return actions.execute_window(False, res_id=ids, model=params.model, domain=params.domain)
        else:
            raise common.message(_('No resource selected !'))

    @expose()
    def open(self, **kw):
        datas = {}

        datas['_terp_model'] = kw.get('model')
        datas['_terp_context'] = kw.get('context', {})
        datas['_terp_domain'] = kw.get('domain', [])

        datas['ids'] = kw.get('id')

        return self.do_action('tree_but_open', datas=datas)
