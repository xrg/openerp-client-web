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
import cherrypy
from openerp.controllers import SecuredController
from openerp.utils import rpc, TinyDict

import openerp.controllers.actions as actions
import openerp.controllers.form as form
from openobject.tools import expose


class Process(SecuredController):

    _cp_path = "/view_diagram/process"

    @expose(template="/view_diagram/controllers/templates/process.mako")
    def default(self, id=False, res_model=None, res_id=False, title=None):

        id = (id or False) and int(id)
        res_id = eval(res_id)

        selection = None
        process_title = None

        fields = rpc.RPCProxy(res_model).fields_get([], {})

        help = 'Help: Not Defined'
        help_ids = rpc.session.execute('object', 'execute', 'ir.actions.act_window', 'search', [('res_model','=',res_model)])
        for help_id in help_ids:
            field = rpc.session.execute('object', 'execute', 'ir.actions.act_window', 'read', help_id)
            if field['help'] and (field['name'] == title):
                help = field['help']

        proxy = rpc.RPCProxy('process.process')
        if id:
            res = proxy.read([id], ['name'], rpc.session.context)[0]
            process_title = res['name']
        else:
            selection = proxy.search_by_model(res_model, rpc.session.context)
            if res_model and not selection:
                selection = proxy.search_by_model(False, rpc.session.context)

            if len(selection) == 1:
                id, process_title = selection[0]
                selection = None

        lang = rpc.session.context.get('lang','en_US')
        context_help='http://doc.openerp.com/index.php?model='+res_model+'&lang='+lang
        return dict(id=id, res_model=res_model, res_id=res_id, title=title, selection=selection, fields=fields, help=help, process_title=process_title, context_help=context_help)

    @expose('json')
    def get(self, id, res_model=None, res_id=False, title=None):

        id = int(id)
        res_id = int(res_id)

        proxy = rpc.RPCProxy('process.process')
        graph = proxy.graph_get(id, res_model, res_id, (80, 80, 150, 100), rpc.session.context)

        related = (res_model or None) and proxy.search_by_model(res_model, rpc.session.context)
        graph['related'] = dict(related or {})

        if graph.get('resource'):
            graph['title'] = _("%(name)s - Resource: %(resource)s, State: %(state)s") % graph
        else:
            graph['title'] = graph['name']

        def update_perm(perm):
            perm = perm or {}

            try:
                perm['date'] = format.format_datetime(perm['write_date'] or perm['create_date'])
            except:
                pass

            perm['text'] = _("Last modified by:")
            perm['value'] = perm.get('write_uid') or perm.get('create_uid')
            if perm['value']:
                perm['value'] =  '%s (%s)' % (perm['value'][1], perm.get('date') or 'N/A')
            else:
                perm['value'] = 'N/A'

            return perm

        # last modified by
        graph['perm'] = update_perm(graph['perm'] or {})
        for nid, node in graph['nodes'].items():
            if not node.get('res'):
                continue
            node['res']['perm'] = update_perm(node['res']['perm'] or {})

        return graph

    @expose(template="/view_diagram/controllers/templates/process_tip.mako")
    def open_tip(self, **kw):
        title_tip = kw.get('title_tip')
        return dict(id=None, res_model=None, res_id=None, title=None, selection=None, title_tip=title_tip)

# vim: ts=4 sts=4 sw=4 si et
