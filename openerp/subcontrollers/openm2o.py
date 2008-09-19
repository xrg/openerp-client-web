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
# along with this program; if not, write to the 
# Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
# Boston, MA  02111-1307, USA.
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

class OpenM2O(Form):
    
    path = '/openm2o'    # mapping from root
    
    @expose(template="openerp.subcontrollers.templates.openm2o")
    def create(self, params, tg_errors=None):

        params.editable = True
        form = self.create_form(params, tg_errors)
        
        form.hidden_fields = [widgets.HiddenField(name='_terp_m2o', default=params.m2o)]

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
        
        # remember the current notebook tab
        cherrypy.session['remember_notebook'] = True

        if tg_errors:
            return self.create(params, tg_errors=tg_errors)

        # bypass save, for button action in non-editable view
        if not (params.button and not params.editable and params.id):

            proxy = rpc.RPCProxy(params.model)

            if not params.id:
                id = proxy.create(data, params.context)
                params.ids = (params.ids or []) + [int(id)]
                params.id = int(id)
                params.count += 1
            else:
                id = proxy.write([params.id], data, params.context)

        button = (params.button or False) and True

        # perform button action
        if params.button:
            res = self.button_action(params)
            if res:
                return res

        current = params.chain_get(params.source or '')
        if current:
            current.id = None
            if not params.id:
                params.id = int(id)
        elif not button:
            params.editable = False

        if not current and not button:
            params.load_counter = 2
            
        return self.create(params)
    
    @expose()    
    def edit(self, **kw):
        params, data = TinyDict.split(kw)
        if not params.model:
            params.update(kw)

        params.view_mode = ['form', 'tree']
        params.view_type = 'form'
        params.editable = True
        return self.create(params)

# vim: ts=4 sts=4 sw=4 si et

