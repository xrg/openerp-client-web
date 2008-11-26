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
import base64

from turbogears import expose
from turbogears import controllers
from turbogears import redirect

from openerp import rpc
from openerp.tinyres import TinyResource
from openerp.utils import TinyDict

import openerp.widgets as tw

class ViewList(controllers.Controller, TinyResource):

    @expose(template="openerp.subcontrollers.templates.viewlist")
    def index(self, model):
        
        params = TinyDict()
        params.model = 'ir.ui.view'
        params.view_mode = ['tree']
        
        params.domain = [('model', '=', model)]
        
        screen = tw.screen.Screen(params, selectable=1)
        screen.widget.pageable = False
        
        return dict(screen=screen, model=model, show_header_footer=False)
    
    @expose()
    def create(self, model, **kw):
        
        view_name = kw.get('name')
        view_type = kw.get('type')
        priority = kw.get('priority', 16)
        
        if not view_name:
            raise redirect('/viewlist', model=model)

        proxy = rpc.RPCProxy(model)
        fields = proxy.fields_get({}).keys()

        fname = None
        for n in ('name', 'x_name'):
            if n in fields:
                fname = n
                break

        if fname:
            arch = """<?xml version="1.0"?>
            <%s string="Unknwown">
                <field name="%s"/>
            </%s>
            """ % (view_type, fname, view_type)

            proxy = rpc.RPCProxy('ir.ui.view')
            proxy.create(dict(model=model, name=view_name, type=view_type, priority=priority, arch=arch))
        
        raise redirect('/viewlist', model=model)
    
    @expose()
    def delete(self, model, id):
        
        id = int(id)
        
        proxy = rpc.RPCProxy('ir.ui.view')
        proxy.unlink(id)
        
        raise redirect('/viewlist', model=model)

# vim: ts=4 sts=4 sw=4 si et

