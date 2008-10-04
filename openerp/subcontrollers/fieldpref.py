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

import os
import time

from turbogears import expose
from turbogears import controllers

import cherrypy

from openerp import rpc
from openerp import tools
from openerp import common

from openerp.tinyres import TinyResource

from openerp.utils import TinyDict
from openerp.utils import TinyForm

import openerp.widgets as tw

class FieldPref(controllers.Controller, TinyResource):
    
    @expose(template="openerp.subcontrollers.templates.fieldpref")
    def index(self, **kw): #_terp_model, _terp_field, _terp_deps
        
        click_ok = None
        params, data = TinyDict.split(kw)
        
        return dict(model=params.model, click_ok=click_ok, field=params.field, deps=params.deps, show_header_footer=False)
    
    @expose('json')
    def get(self, **kw):
        params, data = TinyDict.split(kw)
        
        field = params.field.split('/')
        
        prefix = '.'.join(field[:-1])
        field = field[-1]

        pctx = TinyForm(**kw).to_python()
        ctx = pctx.chain_get(prefix) or pctx
       
        proxy = rpc.RPCProxy(params.model)
        res = proxy.fields_get(False, rpc.session.context)
        
        text = res[field].get('string')
        deps = []
        
        for name, attrs in res.items():
            if attrs.get('change_default', False):
                value = ctx.get(name)
                if value:
                    deps.append((name, name, value, value))
                
        return dict(text=text, deps=str(deps))
    
    @expose(template="openerp.subcontrollers.templates.fieldpref")
    def save(self, **kw):
        params, data = TinyDict.split(kw)
        
        deps = False
        if params.deps:
            for n, v in params.deps.items():
                deps = "%s=%s" %(n,v)
                break

        model = params.model        
        field = params.field['name']        
        value = params.field['value']
        click_ok = 1
        
        field = field.split('/')[-1]

        proxy = rpc.RPCProxy('ir.values')
        res = proxy.set('default', deps, field, [(model,False)], value, True, False, False, params.you or False, True)

        return dict(model=params.model, click_ok=click_ok, field=params.field, deps=params.deps2, should_close=True, show_header_footer=False)

# vim: ts=4 sts=4 sw=4 si et

