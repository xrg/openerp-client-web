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

import cherrypy

from turbogears import expose
from turbogears import controllers

from tinyerp import rpc
from tinyerp.tinyres import TinyResource

from tinyerp.utils import TinyDict
from tinyerp.utils import TinyForm
from tinyerp.utils import TinyFormError

import tinyerp.widgets as tw

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

        model = params.parent.model
        
        if model != params.model and not params.parent.id:
            error = _("Parent record doesn't exists...")

        if error:
            return dict(error=error)

        try:
            proxy = rpc.RPCProxy(model)
            frm = TinyForm(**kw)

            data = {}
            if model != params.model:

                source = params.source
                data = frm.chain_get(source)
                
                if '__id' in data: data.pop('__id')
                
                fld = source.split('/')[-1]
                data = {fld : [(id and 1, id, data.copy())]}                

                proxy.write([params.parent.id], data, params.parent.context or {})
            else:
                data = frm.copy()

                if id > 0:
                    proxy.write([id], data, params.parent.context or {})
                else:
                    proxy.create(data, params.parent.context or {})

        except TinyFormError, e:
            error_field = e.field
            error = ustr(e)
        except Exception, e:
            error = ustr(e)

        return dict(error_field=error_field, error=error)

    @expose('json')
    def remove(self, **kw):
        params, data = TinyDict.split(kw)

        error = None
        proxy = rpc.RPCProxy(params.model)

        if params.id:
            try:
                res = proxy.unlink([params.id])
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

        return dict(ids=str(ids), count=count, view=ustr(wid.render()))
    
    @expose('json')
    def button_action(self, **kw):
        params, data = TinyDict.split(kw)
        
        error = None
        
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
                from tinyerp.subcontrollers import actions
    
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
            
        return dict(error=error)
