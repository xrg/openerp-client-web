###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from turbogears import expose
from turbogears import widgets
from turbogears import validators
from turbogears import validate

import cherrypy

from openerp import rpc
from openerp import cache
from openerp import widgets as tw

from openerp.utils import TinyDict

from form import Form

class OpenO2M(Form):
    
    path = '/openo2m'    # mapping from root
    
    def create_form(self, params, tg_errors=None):
        
        params.id = params.o2m_id
        params.model = params.o2m_model        
        params.view_mode = ['form', 'tree']
        params.view_type = 'form'

        # to get proper view, first generate form using the view_params
        vp = params.view_params
        form = tw.form_view.ViewForm(vp, name="view_form", action="/form/save")
        cherrypy.request.terp_validators = {}
        wid = form.screen.widget.get_widgets_by_name(params.o2m)[0]

        # save view_params for later phazes
        vp = vp.make_plain('_terp_view_params/')
        hiddens = map(lambda x: widgets.HiddenField(name=x, default=vp[x]), vp)

        params.prefix = params.o2m
        params.views = wid.view

        ctx = params.context or {}
        ctx.update(params.o2m_context or {})
        p, ctx = TinyDict.split(ctx)
        
        params.context = ctx or {}

        form = tw.form_view.ViewForm(params, name="view_form", action="/openo2m/save")
        form.hidden_fields = [widgets.HiddenField(name='_terp_parent_model', default=params.parent_model),
                              widgets.HiddenField(name='_terp_parent_id', default=params.parent_id),
                              widgets.HiddenField(name='_terp_o2m', default=params.o2m),                              
                              widgets.HiddenField(name='_terp_o2m_id', default=params.id or None),
                              widgets.HiddenField(name='_terp_o2m_model', default=params.o2m_model),
                              widgets.HiddenField(name=params.prefix + '/__id', default=params.id or None)] + hiddens

        return form
    
    @expose(template="openerp.subcontrollers.templates.openo2m")
    def create(self, params, tg_errors=None):

        if tg_errors:
            form = cherrypy.request.terp_form
        else:
            form = self.create_form(params, tg_errors)        
                
        return dict(form=form, params=params, show_header_footer=False)
    
    def get_form(self):
        params, data = TinyDict.split(cherrypy.request.params)

        # bypass validations, if saving from button in non-editable view
        if params.button and not params.editable and params.id:
            return None

        cherrypy.request.terp_validators = {}

        params.nodefault = True

        form = self.create_form(params)
        cherrypy.request.terp_form = form

        vals = cherrypy.request.terp_validators
        schema = validators.Schema(**vals)

        form.validator = schema

        return form
    
    @expose()
    @validate(form=get_form)
    def save(self, terp_save_only=False, tg_errors=None, **kw):
        params, data = TinyDict.split(kw)
        params.editable = True

        if tg_errors:
            return self.create(params, tg_errors=tg_errors)
       
        proxy = rpc.RPCProxy(params.parent_model)

        pprefix = '.'.join(params.o2m.split('/')[:-1])

        if pprefix:
            data = eval(pprefix, TinyDict(**data)).make_dict()

        id = proxy.write([params.parent_id], data, rpc.session.context)
        
        params.load_counter = 1

        prefix = params.o2m
        current = params.chain_get(prefix)

        if current and current.id:
            params.load_counter = 2

        return self.create(params)
    
    @expose()
    def edit(self, **kw):
        params, data = TinyDict.split(kw)
        return self.create(params)

# vim: ts=4 sts=4 sw=4 si et

