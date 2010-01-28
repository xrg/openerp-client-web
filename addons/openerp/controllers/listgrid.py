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

import cherrypy

from openobject.tools import expose

from openerp.utils import rpc
from openerp.utils import TinyDict
from openerp.utils import TinyForm
from openerp.utils import TinyFormError
from openerp.utils import context_with_concurrency_info

from openerp.controllers import SecuredController

from openerp.widgets import listgrid

import form
import search
import wizard

class List(SecuredController):
    
    _cp_path = "/listgrid"

    @expose('json')
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

            if model != params.model:
                source = params.source
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

    @expose('json')
    def remove(self, **kw):
        params, data = TinyDict.split(kw)
        error = None
        proxy = rpc.RPCProxy(params.model)
        if params.ids:
            try:
                ctx = context_with_concurrency_info(params.context, params.concurrency_info)
                if isinstance(params.ids, list):
                    res = proxy.unlink(params.ids, ctx)
                else:
                    res = proxy.unlink([params.ids], ctx)
            except Exception, e:
                error = ustr(e)

        return dict(error=error)

    @expose('json')
    def get(self, **kw):
        params, data = TinyDict.split(kw)

        params.ids = None
        source = (params.source or '') and str(params.source)

        params.view_type = 'form'

        if source == '_terp_list':
            params.view_type = 'tree'
            if params.search_domain:
                params.domain += params.search_domain

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

        wid = frm.screen.get_widgets_by_name(source, kind=listgrid.List)[0]
        ids = wid.ids
        count = wid.count

        if params.edit_inline:
            wid.edit_inline = params.edit_inline

        info = {}
        if params.concurrency_info:
            for m, v in getattr(cherrypy.request, 'terp_concurrency_info', {}).items():
                for i, d in v.items():
                    info['%s,%s' % (m, i)] = d

        return dict(ids=ids, count=count, view=ustr(wid.render()), info=info)

    @expose('json')
    def button_action(self, **kw):
        params, data = TinyDict.split(kw)

        error = None
        reload = (params.context or {}).get('reload', False)
        result = {}

        name = params.button_name
        btype = params.button_type

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
                if isinstance(res, dict) and res.get('type') == 'ir.actions.act_url':
                    result = res

            elif btype == 'action':
                import actions

                action_id = int(name)
                action_type = actions.get_action_type(action_id)

                if action_type == 'ir.actions.wizard':
                    cherrypy.session['wizard_parent_form'] = '/form'
                    cherrypy.session['wizard_parent_params'] = params

                res = actions.execute_by_id(action_id, type=action_type, model=model, id=id, ids=ids)
                if isinstance(res, dict) and res.get('type') == 'ir.actions.act_url':
                    result = res
                elif res:
                    error = "Button action has returned another view..."

            else:
                error = "Unallowed button type"
        except Exception, e:
            error = ustr(e)

        return dict(error=error, result=result, reload=reload)
    
    @expose('json')
    def sort_by_drag(self, **kw):
        params, data = TinyDict.split(kw)
        id = params.id
        ids = params.ids or []
        proxy = rpc.RPCProxy(params.model)
        ctx = rpc.session.context.copy()
        swap_id = params.swap_id
        
        res_id = proxy.read([id], ['sequence'], ctx)[0]
        id_seq = res_id['sequence']
        res_swap_id = proxy.read([swap_id], ['sequence'], ctx)[0]
        swap_id_seq = res_swap_id['sequence']
        if id_seq<= swap_id_seq:
            new_ids = []
            if ids[ids.index(id)+1: ids.index(swap_id)]:
                new_ids.extend(ids[ids.index(id)+1: ids.index(swap_id)+1])
                new_ids.append(id)
            else:
                new_ids.append(id)
                new_ids.extend(ids[ids.index(swap_id): ids.index(id)])

            res = proxy.read(new_ids,['sequence'], ctx)
            if swap_id_seq < len(new_ids):
                for r in res:
                    if r['id'] == id:
                        proxy.write([r['id']], {'sequence': len(new_ids)}, ctx)
                    else:
                        proxy.write([r['id']], {'sequence': ids.index(r['id'])}, ctx)
                        
            else:
                for r in res:
                    if r['id'] == id:
                        proxy.write([r['id']], {'sequence': swap_id_seq}, ctx)
                    else:
                        proxy.write([r['id']], {'sequence': r['sequence'] -1}, ctx)
        
        else:
            new_ids = []
            new_ids.append(id)
            new_ids.extend(ids[ids.index(swap_id): ids.index(id)])
            res = proxy.read(new_ids,['sequence'], ctx)
            for r in res:
                if r['id'] == id:
                    proxy.write([r['id']], {'sequence': swap_id_seq}, ctx)
                else:
                    proxy.write([r['id']], {'sequence': ids.index(r['id'])+2}, ctx)
        
        return dict()
    
    @expose('json')
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

    @expose('json')
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

