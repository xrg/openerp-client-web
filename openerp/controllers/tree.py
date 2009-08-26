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

"""
This module implementes heirarchical tree view for a tiny model having
    view_type = 'tree'
"""

import time
import xml.dom.minidom

from openerp.tools import expose
from openerp.tools import url

from openerp import rpc
from openerp import icons
from openerp import tools
from openerp import common
from openerp import cache

from openerp.controllers.base import SecuredController
from openerp.widgets import tree_view

from openerp.utils import TinyDict

DT_FORMAT = '%Y-%m-%d'
DHM_FORMAT = '%Y-%m-%d %H:%M:%S'

class Tree(SecuredController):

    @expose(template="templates/tree.mako")
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
                if tool.get('icon'):
                    tool['icon'] = icons.get_icon(tool['icon'])
                else:
                    tool['icon'] = False

        return dict(tree=tree, model=model)

    @expose()
    def default(self, id, model, view_id, domain, context):
        params = TinyDict()

        try:
            view_id = int(view_id)
        except:
            view_id = False

        params.ids = id
        params.view_ids = [view_id]
        params.model = model
        params.domain = domain
        params.context = context or {}

        return self.create(params)

    def sort_callback(self, item1, item2, field, sort_order="asc"):
        a = item1[field]
        b = item2[field]

        if(sort_order == "dsc"):
            return -cmp(a, b)

        return cmp(a, b)

    @expose('json')
    def data(self, ids, model, fields, field_parent=None, icon_name=None, domain=[], context={}, sort_by=None, sort_order="asc"):

        ids = ids or []

        if isinstance(ids, basestring):
            ids = [int(id) for id in ids.split(',')]

        if isinstance(fields, basestring):
            fields = eval(fields)

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
            record['action'] = url('/tree/open', model=model, id=record['id'])
            record['target'] = None

            record['icon'] = None

            if icon_name and item.get(icon_name):
                icon = item.pop(icon_name)
                record['icon'] = icons.get_icon(icon)

                if icon == 'STOCK_OPEN':
                    record['action'] = None
                    record['target'] = None

            record['children'] = []

            if field_parent and field_parent in item:
                record['children'] = item.pop(field_parent) or None

            record['items'] = item

            records += [record]

        return dict(records=records)

    def do_action(self, name, adds={}, datas={}):
        params, data = TinyDict.split(datas)

        model = params.model
        context = params._terp_context or {}
        ids = data.get('ids') or []

        ctx = rpc.session.context.copy()
        ctx.update(context)

        if ids:
            ids = [int(id) for id in ids.split(',')]

        id = (ids or False) and ids[0]

        if len(ids):
            from openerp.controllers import actions
            return actions.execute_by_keyword(name, adds=adds, model=model, id=id, ids=ids, context=ctx, report_type='pdf')
        else:
            raise common.message(_("No record selected!"))

    @expose()
    def report(self, **kw):
        return self.do_action('client_print_multi', datas=kw)

    @expose()
    def action(self, **kw):
        params, data = TinyDict.split(kw)

        action = params.data

        if not action:
            return self.do_action('tree_but_action', datas=kw)

        from openerp.controllers import actions

        ids = params.selection or []
        id = (ids or False) and ids[0]

        return actions.execute(action, model=params.model, id=id, ids=ids, report_type='pdf')

    @expose()
    def switch(self, **kw):

        params, data = TinyDict.split(kw)

        ids = params.selection or []            
        if len(ids):
            from openerp.controllers import actions
            return actions.execute_window(False, res_id=ids, model=params.model, domain=params.domain)
        else:
            raise common.message(_('No resource selected!'))

    @expose()
    def open(self, **kw):
        datas = {}

        datas['_terp_model'] = kw.get('model')
        datas['_terp_context'] = kw.get('context', {})
        datas['_terp_domain'] = kw.get('domain', [])

        datas['ids'] = kw.get('id')

        return self.do_action('tree_but_open', datas=datas)

# vim: ts=4 sts=4 sw=4 si et

