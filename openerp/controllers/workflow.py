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

from openerp.tools import expose
from openerp.tools import redirect
from openerp.tools import validate

import pkg_resources
import cherrypy

from openerp import rpc
from openerp import common

from openerp.utils import TinyDict
from openerp.controllers.base import SecuredController

from openerp import widgets as tw

from form import Form


#rpc.session = rpc.RPCSession('localhost', '8070', 'socket', storage=cherrypy.session)

class State(Form):

    path = '/workflow/state'    # mapping from root

    @expose(template="templates/wkf_popup.mako")
    def create(self, params, tg_errors=None):

        params.path = self.path
        params.function = 'create_state'

        if params.id and cherrypy.request.path_info == self.path + '/view':
            params.load_counter = 2

        params.hidden_fields = [tw.form.Hidden(name='wkf_id', default=params.wkf_id)]
        form = self.create_form(params, tg_errors)

        field = form.screen.widget.get_widgets_by_name('wkf_id')[0]
        field.set_value(params.wkf_id or False)
        field.readonly = True

        vals = getattr(cherrypy.request, 'terp_validators', {})
        vals['wkf_id'] = tw.validators.Int()

        hide = []

        hide += form.screen.widget.get_widgets_by_name('out_transitions')
        hide += form.screen.widget.get_widgets_by_name('in_transitions')
        hide += form.screen.widget.get_widgets_by_name('', kind=tw.form.Separator)

        for w in hide:
            w.visible = False

        return dict(form=form, params=params)

    @expose()
    def edit(self, **kw):

        params, data = TinyDict.split(kw)

        if not params.model:
            params.update(kw)

        params.view_mode = ['form']
        params.view_type = 'form'
        params.editable = True

        return self.create(params)

    @expose()
    def delete(self, id, **kw):

        error_msg = None
        proxy = rpc.RPCProxy('workflow.activity')
        res_act = proxy.unlink(int(id))

        if not res_act:
            error_msg = _('Could not delete state')

        return dict(error = error_msg)

    @expose('json')
    def get_info(self, id, **kw):

        proxy_act = rpc.RPCProxy('workflow.activity')
        search_act = proxy_act.search([('id', '=', int(id))], 0, 0, 0, rpc.session.context)
        data = proxy_act.read(search_act, [], rpc.session.context)

        return dict(data=data[0])

class Connector(Form):

    path = '/workflow/connector'    # mapping from root

    @expose(template="templates/wkf_popup.mako")
    def create(self, params, tg_errors=None):

        params.path = self.path
        params.function = 'update_connection'

        if params.id and cherrypy.request.path_info == self.path + '/view':
            params.load_counter = 2

        params.hidden_fields = [tw.form.Hidden(name='act_from', default=params.start),
                                tw.form.Hidden(name='act_to', default=params.end)]

        form = self.create_form(params, tg_errors)

        field_act_from = form.screen.widget.get_widgets_by_name('act_from')[0]
        field_act_from.set_value(params.start or False)
        field_act_from.readonly = True

        field_act_to = form.screen.widget.get_widgets_by_name('act_to')[0]
        field_act_to.set_value(params.end or False)
        field_act_to.readonly = True

        vals = getattr(cherrypy.request, 'terp_validators', {})
        vals['act_from'] = tw.validators.Int()
        vals['act_to'] = tw.validators.Int()

        return dict(form=form, params=params)

    @expose()
    def edit(self, **kw):

        params, data = TinyDict.split(kw)

        if not params.model:
            params.update(kw)

        params.view_mode = ['form']
        params.view_type = 'form'
        params.editable = True

        return self.create(params)

    @expose('json')
    def delete(self, id, **kw):

        error_msg = None
        proxy = rpc.RPCProxy('workflow.transition')
        res_tr = proxy.unlink(int(id))

        if not res_tr:
            error_msg = _('Could not delete state')

        return dict(error=error_msg)

    @expose('json')
    def auto_create(self, act_from, act_to, **kw):

        proxy_tr = rpc.RPCProxy('workflow.transition')
        id = proxy_tr.create({'act_from': act_from, 'act_to': act_to})
        data = proxy_tr.read(id, [], rpc.session.context);

        if id>0:
            return dict(flag=True,data=data)
        else:
            return dict(flag=False)

    @expose('json')
    def get_info(self, id, **kw):

        proxy_tr = rpc.RPCProxy('workflow.transition')
        search_tr = proxy_tr.search([('id', '=', int(id))], 0, 0, 0, rpc.session.context)
        data = proxy_tr.read(search_tr, [], rpc.session.context)

        return dict(data=data[0])

    @expose('json')
    def change_ends(self, id, field, value):

        proxy_tr = rpc.RPCProxy('workflow.transition')
        id = proxy_tr.write([int(id)], {field: int(value)}, rpc.session.context)
        return dict()


class Workflow(Form):

    path = '/workflow'

    @expose(template="templates/workflow.mako")
    def index(self, model, id=None):

        proxy = rpc.RPCProxy("workflow")
        if id:
            ids = proxy.search([('id', '=', id)], 0, 0, 0, rpc.session.context)
        else:
            ids = proxy.search([('osv', '=', model)], 0, 0, 0, rpc.session.context)

        if not ids:
            raise common.message(_('No workflow associated!'))

        wkf = proxy.read(ids, [], rpc.session.context)[0]
        return dict(wkf=wkf)

    @expose('json')
    def get_info(self, id, **kw):

        proxy = rpc.RPCProxy("workflow")
        search_ids = proxy.search([('id', '=' , int(id))], 0, 0, 0, rpc.session.context)
        graph_search = proxy.graph_get(search_ids[0], (140, 180), rpc.session.context)

        nodes = graph_search['nodes']
        transitions = graph_search['transitions']

        connectors = {}
        list_tr = [];

        for tr in transitions:
            list_tr.append(tr)
            t = connectors.setdefault(tr,{})
            t['id'] = tr
            t['s_id'] = transitions[tr][0]
            t['d_id'] = transitions[tr][1]

        proxy_tr = rpc.RPCProxy("workflow.transition")
        search_trs = proxy_tr.search([('id', 'in', list_tr)], 0, 0, 0, rpc.session.context)
        data_trs = proxy_tr.read(search_trs, ['signal', 'condition', 'act_from', 'act_to'], rpc.session.context)

        for tr in data_trs:
            t = connectors.get(tr['id'])
            t['signal'] = tr['signal']
            t['condition'] = tr['condition']
            t['source'] = tr['act_from'][1]
            t['destination'] = tr['act_to'][1]

        proxy_act = rpc.RPCProxy("workflow.activity")
        search_acts = proxy_act.search([('wkf_id', '=', int(id))], 0, 0, 0, rpc.session.context)
        data_acts = proxy_act.read(search_acts, ['action', 'kind', 'flow_start', 'flow_stop', 'subflow_id'], rpc.session.context)

        for act in data_acts:
            n = nodes.get(str(act['id']))
            n['id'] = act['id']
            n['flow_start'] = act['flow_start']
            n['flow_stop'] = act['flow_stop']
            n['action'] = act['action']
            n['kind'] = act['kind']
            n['subflow_id'] = act['subflow_id']

        return dict(nodes=nodes,conn=connectors)

    state = State()
    connector = Connector()


class WorkflowList(SecuredController):

    @expose(template="templates/wkf_list.mako")
    def index(self, model, active=False):

        params = TinyDict()
        params.model = 'workflow'
        params.view_mode = ['tree']

        params.domain = [('osv', '=', model)]

        screen = tw.screen.Screen(params, selectable=1)
        screen.widget.pageable = False

        return dict(screen=screen, model=model, active=active)

    @expose()
    def create(self, model, **kw):

        wkf_name = kw.get('name')
        on_create = kw.get('on_create')

        if not wkf_name:
            raise redirect('/workflowlist', model=model)

        proxy = rpc.RPCProxy('workflow')
        proxy.create(dict(osv=model, name=wkf_name, on_create=on_create))

        raise redirect('/workflowlist', model=model)

    @expose()
    def delete(self, model, id):

        id = int(id)

        proxy = rpc.RPCProxy('workflow')
        proxy.unlink(id)

        raise redirect('/workflowlist', model=model)

    @expose()
    def activate(self, model, id):

        activate_id = int(id)

        proxy = rpc.RPCProxy('workflow')
        search_ids = proxy.search([('osv', '=', model)], 0, 0, 0, rpc.session.context)

        for id in search_ids:
            if id==activate_id:
                proxy.write([id], {'on_create': True})
            else:
                proxy.write([id], {'on_create': False})

        raise redirect('/workflowlist', model=model)

# vim: ts=4 sts=4 sw=4 si et


