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

import cherrypy
from openerp.controllers import SecuredController
from openerp.utils import rpc, TinyDict, TinyForm, TinyFormError, context_with_concurrency_info, cache
from openerp.widgets import listgrid, listgroup

import form
import wizard
from openobject.tools import expose, ast

class List(SecuredController):

    _cp_path = "/openerp/listgrid"

    @expose('json', methods=('POST',))
    def save(self, **kw):
        params, data = TinyDict.split(kw)

        error = None
        error_field = None

        id = params.id or 0
        id = (id > 0) and id or 0

        ids = params.ids or []

        model = params.parent.model
        if model != params.model and not params.parent.id:
            error = _("Parent record doesn't exists...")

        if error:
            return dict(error=error)

        try:
            proxy = rpc.RPCProxy(model)
            frm = TinyForm(**kw).to_python()
            data = {}
            ctx = context_with_concurrency_info(params.parent.context, params.concurrency_info)

            source = params.source
            if source and source != '_terp_list':

                data = frm.chain_get(source)

                if '__id' in data: data.pop('__id')
                if 'id' in data: data.pop('id')

                fld = source.split('/')[-1]
                data = {fld : [(id and 1, id, data.copy())]}
                proxy.write([params.parent.id], data, ctx)

                all_ids = proxy.read([params.parent.id], [fld])[0][fld]
                new_ids = [i for i in all_ids if i not in ids]

                ids = all_ids
                if new_ids:
                    id = new_ids[0]

            else:
                data = frm.copy()
                if 'id' in data: data.pop('id')

                if id > 0:
                    proxy.write([id], data, ctx)
                else:
                    id = proxy.create(data, params.parent.context or {})
                    ids = [id] + ids

        except TinyFormError, e:
            error_field = e.field
            error = ustr(e)
        except Exception, e:
            error = ustr(e)

        return dict(error_field=error_field, error=error, id=id, ids=str([int(i) for i in ids]))

    @expose('json', methods=('POST',))
    def remove(self, **kw):
        params, data = TinyDict.split(kw)
        sc_ids = [i['id'] for i in cherrypy.session['terp_shortcuts']]
        error = None
        proxy = rpc.RPCProxy(params.model)
        if params.id:

            if params.model == 'ir.ui.view_sc' and cherrypy.session.get('terp_shortcuts'):
                for sc in cherrypy.session.get('terp_shortcuts'):
                    for id in params.id:
                        if id == sc['id']:
                            cherrypy.session['terp_shortcuts'].remove(sc)

            try:
                ctx = context_with_concurrency_info(params.context, params.concurrency_info)
                if isinstance(params.id, list):
                    res = proxy.unlink(params.id, ctx)
                    for i in params.id:
                        params.ids.remove(i)
                else:
                    res = proxy.unlink([params.id], ctx)
                    params.ids.remove(params.id)
                
                if params.model == 'res.request':
                    ids, ids2 = rpc.RPCProxy(params.model).request_get()
                    return dict(res_ids = ids)
                
                return dict(ids = params.ids, count = len(params.ids))
            except Exception, e:
                error = ustr(e)

        return dict(error=error)

    @expose('json', methods=('POST',))
    def remove_o2m_defaults(self, o2m_value, index):
        o2m_value = eval(o2m_value)
        o2m_value.pop(int(index))
        return dict(o2m_value=ustr(o2m_value))

    @expose('json')
    def get_o2m_defaults(self, o2m_values, model, o2m_model, name, view_type, view_id,
                         o2m_view_type, o2m_view_id, editable, limit, offset, o2m_context, o2m_domain):

        view_id = view_id or False
        o2m_view_id = eval(o2m_view_id) or False

        context = dict((eval(o2m_context) or {}), **rpc.session.context)

        import simplejson
        o2m_values = simplejson.loads(o2m_values)

        if o2m_values and isinstance(o2m_values, unicode):
            o2m_values = eval(o2m_values)

        for o2m in o2m_values:
            o2m['id'] = 0

        if o2m_view_id:
            view = cache.fields_view_get(o2m_model, o2m_view_id, o2m_view_type, context)
        else:
            view = cache.fields_view_get(model, view_id, view_type, rpc.session.context)
            view = view['fields'].get(name).get('views').get(o2m_view_type)

        list_view = listgrid.List(name, model, view, ids=None, domain=o2m_domain, context=context, default_data=copy.deepcopy(o2m_values), limit=20, editable= editable,o2m=1)
        view=ustr(list_view.render())
        formated_o2m_values = []
        for o2m in o2m_values:
            o2m.pop('id', None)
            formated_o2m_values.append((0, 0, o2m))

        return dict(view=view, formated_o2m_values=ustr(formated_o2m_values))

    @expose()
    def multiple_groupby(self, model, name, grp_domain, group_by, view_id, view_type, parent_group, group_level, groups, no_leaf, **kw):
        grp_domain = ast.literal_eval(grp_domain)
        view = cache.fields_view_get(model, view_id, view_type, rpc.session.context.copy())
        group_by = ast.literal_eval(group_by)
        domain = grp_domain
        group_level = ast.literal_eval(group_level)
        groups = ast.literal_eval(groups)

        context = {'group_by_no_leaf': int(no_leaf), 'group_by': group_by, '__domain': domain}
        args = {'editable': True,
                'view_mode': ['tree', 'form', 'calendar', 'graph'],
                'nolinks': 1, 'group_by_ctx': group_by,
                'selectable': 2,
                'multiple_group_by': True,
                'sort_key': kw.get('sort_key'),
                'sort_order': kw.get('sort_order')}

        listgrp = listgroup.MultipleGroup(name, model, view, ids=None, domain= domain, parent_group=parent_group, group_level=group_level, groups=groups, context=context, **args)
        return listgrp.render()

    @expose('json')
    def reload_graph(self, **kw):
        params, data = TinyDict.split(kw)
        view = cache.fields_view_get(params.model, params.view_id, 'graph',params.context)
        
        if params.group_by_ctx:
            if isinstance(params.group_by_ctx, str):
                params.group_by_ctx = params.group_by_ctx.split('group_')[-1]
            else:
                params.group_by_ctx = map(lambda x: x.split('group_')[-1], params.group_by_ctx)
        
        if params.domain is None:
            params.domain = []
        if params.search_domain:
            params.domain.extend(params.search_domain)
        if not params.group_by_ctx:
            params.ids = None
        from view_graph.widgets import _graph
        wid = _graph.Graph(model=params.model,
              view=view,
              view_id=params.view_id,
              ids=params.ids, domain=params.domain,
              view_mode = params.view_mode,
              context=params.context,
              group_by = params.group_by_ctx)
        view=ustr(wid.render())
        return dict(view = view)
    
    @expose('jsonp', methods=('POST',))
    def get(self, **kw):
        params, data = TinyDict.split(kw)

        groupby = params.get('_terp_group_by_ctx')
        if groupby and isinstance(groupby, basestring):
            groupby = groupby.split(',')

        if params.get('_terp_filters_context'):
            if isinstance(params.filters_context, (list, tuple)):
                for filter_ctx in params.filters_context:
                    params.context.update(filter_ctx)
            else:
                params.context.update(params.filters_context)

        params['_terp_group_by_ctx'] = groupby
        if not params.search_text:
            params.ids = None

        source = (params.source or '') and str(params.source)
        if not params.view_type == 'graph':
            params.view_type = 'form'

        if params.get('_terp_clear'):
            params.search_domain, params.filter_domain, params.ids = [], [], []
            params.search_data = {}
            for k,v in params.context.items():
                if k.startswith('search_default'):
                    params.context[k] = 0

            if params.context.get('group_by_no_leaf'):
                params.context['group_by_no_leaf'] = 0
            if params.context.get('group_by'):
                params.context['group_by'] = []
            params.group_by_ctx = groupby = []

        if source == '_terp_list':
            if not params.view_type == 'graph':
                params.view_type = 'tree'
            if params.search_domain:
                params.domain += params.search_domain
                
            params.domain = params.domain or []
            if params.filter_domain:
                params.domain += params.filter_domain

        # default_get context
        current = params.chain_get(source)
        if current and params.source_default_get:
            current.context = current.context or {}
            current.context.update(params.source_default_get)

        if params.wiz_id:
            res = wizard.Wizard().execute(params)
            frm = res['form']
        else:
            frm = form.Form().create_form(params)

        if params.view_type == 'graph':
            wid = frm.screen.widget
        else:
            wid = frm.screen.get_widgets_by_name(source, kind=listgrid.List)[0]

        ids = wid.ids
        count = wid.count

        if params.edit_inline:
            wid.edit_inline = params.edit_inline

        info = {}
        if params.concurrency_info:
            info = getattr(cherrypy.request, 'terp_concurrency_info', {})

        if params.get('_terp_clear'):
            view=ustr(frm.render())
        else:
            view=ustr(wid.render())

        server_logs = ''

        if frm.logs and frm.screen.view_type == 'tree':
            server_logs = ustr(frm.logs.render())
        return dict(ids=ids, count=count, view=view, info=info, logs=server_logs)

    @expose('json')
    def button_action(self, **kw):
        params, data = TinyDict.split(kw)

        error = None
        reload = (params.context or {}).get('reload', False)
        result = {}

        name = params.button_name
        btype = params.button_type
        ctx = dict((params.context or {}), **rpc.session.context)

        id = params.id
        model = params.model

        id = (id or False) and int(id)
        ids = (id or []) and [id]

        try:

            if btype == 'workflow':
                rpc.session.execute('object', 'exec_workflow', model, name, id)

            elif btype == 'object':
                ctx = params.context or {}
                ctx.update(rpc.session.context.copy())
                res = rpc.session.execute('object', 'execute', model, name, ids, ctx)
                
                if isinstance(res, dict) and res.get('type'):
                    if  res['type'] == 'ir.actions.act_url':
                        result = res
                    elif res['type'] == 'ir.actions.act_window':
                        import actions
                        res  = actions.execute(res)
                        return dict(res = res)
                        
            elif btype == 'action':
                import actions

                action_id = int(name)
                action_type = actions.get_action_type(action_id)

                if action_type == 'ir.actions.wizard':
                    cherrypy.session['wizard_parent_form'] = '/form'
                    cherrypy.session['wizard_parent_params'] = params

                res = actions.execute_by_id(action_id, type=action_type, model=model, id=id, ids=ids, context=ctx or {})
                if isinstance(res, dict) and res.get('type') == 'ir.actions.act_url':
                    result = res
                elif isinstance(res, basestring):
                    return dict(res = res)
                else:
                    error = "Button action has returned another view.."

            else:
                error = "Unallowed button type"
        except Exception, e:
            error = ustr(e)

        return dict(error=error, result=result, reload=reload)

    @expose('json', methods=('POST',))
    def groupbyDrag(self, model, children, domain):
        domain = ast.literal_eval(domain)[0]
        children = ast.literal_eval(children)
        if isinstance(children, list):
            children = list(children)
        else:
            children = [children]
        rpc.RPCProxy(model).write(children, {domain[0]: domain[2]})
        return {}

    @expose('json', methods=('POST',))
    def dragRow(self, **kw):
        params, data = TinyDict.split(kw)
        id = params.id
        swap_id = params.swap_id
        ids = params.ids

        proxy = rpc.RPCProxy(params.model)
        ctx = rpc.session.context.copy()

        res_ids = []
        if ids.index(id) < ids.index(swap_id):
            if ids[:ids.index(id)]:
                res_ids.extend(ids[:ids.index(id)])
            if ids[ids.index(id)+1:ids.index(swap_id)+1]:
                res_ids.extend(ids[ids.index(id)+1:ids.index(swap_id)+1])
            res_ids.append(id)
            if ids[ids.index(swap_id)+1:]:
                res_ids.extend(ids[ids.index(swap_id)+1:])
        else:
            if ids[:ids.index(swap_id)]:
                res_ids.extend(ids[:ids.index(swap_id)])
            res_ids.append(id)
            if ids[ids.index(swap_id):ids.index(id)]:
                res_ids.extend(ids[ids.index(swap_id):ids.index(id)])
            if ids[ids.index(id)+1:]:
                res_ids.extend(ids[ids.index(id)+1:])

        res = proxy.read(res_ids, ['sequence'], ctx)
        for r in res:
            proxy.write([r['id']], {'sequence': res_ids.index(r['id'])+1}, ctx)
        return dict()

    @expose('json')
    def count_sum(self, model, ids, sum_fields):
        selected_ids = ast.literal_eval(ids)
        sum_fields = sum_fields.split(",")
        ctx = rpc.session.context.copy()

        proxy = rpc.RPCProxy(model)
        res = proxy.read(selected_ids, sum_fields, ctx)

        total = []
        for field in sum_fields:
           total.append([])

        for i in range(len(selected_ids)):
            for k in range(len(sum_fields)):
                total[k].append(res[i][sum_fields[k]])

        total_sum = []
        for s in total:
            total_sum.append(str(sum(s)))

        return dict(sum = total_sum)

    @expose('json', methods=('POST',))
    def moveUp(self, **kw):

        params, data = TinyDict.split(kw)

        id = params.id
        ids = params.ids or []
        if id not in ids or ids.index(id) == 0:
            return dict()

        proxy = rpc.RPCProxy(params.model)
        ctx = rpc.session.context.copy()

        prev_id = ids[ids.index(id)-1]

        try:
            res = proxy.read([id, prev_id], ['sequence'], ctx)
            records = dict([(r['id'], r['sequence']) for r in res])
            cur_seq = records[id]
            prev_seq = records[prev_id]
            if cur_seq == prev_seq:
                proxy.write([prev_id], {'sequence': cur_seq + 1}, ctx)
                proxy.write([id], {'sequence': prev_seq}, ctx)
            else:
                proxy.write([id], {'sequence': prev_seq}, ctx)
                proxy.write([prev_id], {'sequence': cur_seq}, ctx)

            return dict()
        except Exception, e:
            return dict(error=str(e))

    @expose('json', methods=('POST',))
    def moveDown(self, **kw):
        params, data = TinyDict.split(kw)

        id = params.id
        ids = params.ids or []

        if id not in ids or ids.index(id) == len(ids) - 1:
            return dict()

        proxy = rpc.RPCProxy(params.model)
        ctx = rpc.session.context.copy()

        next_id = ids[ids.index(id)+1]

        try:
            res = proxy.read([id, next_id], ['sequence'], ctx)
            records = dict([(r['id'], r['sequence']) for r in res])

            cur_seq = records[id]
            next_seq = records[next_id]

            if cur_seq == next_seq:
                proxy.write([next_id], {'sequence': cur_seq + 1}, ctx)
                proxy.write([id], {'sequence': next_seq}, ctx)
            else:
                proxy.write([id], {'sequence': next_seq}, ctx)
                proxy.write([next_id], {'sequence': cur_seq}, ctx)

            return dict()
        except Exception, e:
            return dict(error=str(e))

# vim: ts=4 sts=4 sw=4 si et

