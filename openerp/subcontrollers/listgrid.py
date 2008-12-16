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

from turbogears import expose
from turbogears import controllers

from openerp import rpc
from openerp.tinyres import TinyResource

from openerp.utils import TinyDict
from openerp.utils import TinyForm
from openerp.utils import TinyFormError

import openerp.widgets as tw

import form
import search

class List(controllers.Controller, TinyResource):

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
            
            if model != params.model:
                source = params.source
                data = frm.chain_get(source)
                
                if '__id' in data: data.pop('__id')
                if 'id' in data: data.pop('id')
                
                fld = source.split('/')[-1]
                data = {fld : [(id and 1, id, data.copy())]}

                proxy.write([params.parent.id], data, params.parent.context or {})

                all_ids = proxy.read([params.parent.id], [fld])[0][fld]
                new_ids = [i for i in all_ids if i not in ids]

                ids = all_ids
                if new_ids:
                    id = new_ids[0]

            else:
                data = frm.copy()
                if 'id' in data: data.pop('id')

                if id > 0:
                    proxy.write([id], data, params.parent.context or {})
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
                if isinstance(params.ids, list):                    
                    res = proxy.unlink(params.ids)
                else:
                    res = proxy.unlink([params.ids])
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

        frm = form.Form().create_form(params)

        wid = frm.screen.get_widgets_by_name(source, kind=tw.listgrid.List)[0]
        ids = wid.ids
        count = wid.count
        
        if params.edit_inline:
            wid.edit_inline = params.edit_inline
            
        return dict(ids=ids, count=count, view=ustr(wid.render()))
    
    @expose('json')
    def button_action(self, **kw):
        params, data = TinyDict.split(kw)
        
        error = None
        reload = (params.context or {}).get('reload', False)

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
                rpc.session.execute('object', 'execute', model, name, ids, ctx)
    
            elif btype == 'action':
                from openerp.subcontrollers import actions
    
                action_id = int(name)
                action_type = actions.get_action_type(action_id)
    
                if action_type == 'ir.actions.wizard':
                    cherrypy.session['wizard_parent_form'] = params
    
                res = actions.execute_by_id(action_id, type=action_type, model=model, id=id, ids=ids)
                if res:
                    raise "Button action has returned another view..."
    
            else:
                raise 'Unallowed button type'
        except Exception, e:
            error = ustr(e)
            
        return dict(error=error, reload=reload)
    
    @expose('json')
    def moveUp(self, **kw):
        params, data = TinyDict.split(kw)
        
        cur_seq = params.get('_terp_cur_seq')
        prev_seq = params.get('_terp_prev_seq')
        model = params.get('_terp_model')
        cur_id = params.get('_terp_cur_id')
        prev_id = params.get('_terp_prev_id')
        
        proxy = rpc.RPCProxy(model)
        
        if cur_seq == prev_seq:
            proxy.write([prev_id], {'sequence': cur_seq + 1}, rpc.session.context)
            proxy.write([cur_id], {'sequence': prev_seq}, rpc.session.context)
        else:            
            proxy.write([prev_id], {'sequence': cur_seq}, rpc.session.context)
            proxy.write([cur_id], {'sequence': prev_seq}, rpc.session.context)
        
        return dict()
    
    @expose('json')
    def moveDown(self, **kw):
        params, data = TinyDict.split(kw)
        
        cur_seq = params.get('_terp_cur_seq')
        next_seq = params.get('_terp_next_seq')
        model = params.get('_terp_model')
        cur_id = params.get('_terp_cur_id')
        next_id = params.get('_terp_next_id')
        
        proxy = rpc.RPCProxy(model)
        
        if cur_seq == next_seq:
            proxy.write([next_id], {'sequence': cur_seq + 1}, rpc.session.context)
            proxy.write([cur_id], {'sequence': next_seq}, rpc.session.context)
        else:
            proxy.write([next_id], {'sequence': cur_seq}, rpc.session.context)
            proxy.write([cur_id], {'sequence': next_seq}, rpc.session.context)
            
        return dict()
    
    @expose('json')
    def assign_seq(self, **kw):
        params, data = TinyDict.split(kw)
        
        model = params.get('_terp_model')
        proxy = rpc.RPCProxy(model)
        
        for i, id in enumerate(params.ids):
            proxy.write([id], {'sequence': i}, rpc.session.context)
        
        return dict()
        
# vim: ts=4 sts=4 sw=4 si et

