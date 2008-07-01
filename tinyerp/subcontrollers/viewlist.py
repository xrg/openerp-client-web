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

import os
import base64

from turbogears import expose
from turbogears import controllers
from turbogears import redirect

from tinyerp import rpc
from tinyerp.tinyres import TinyResource
from tinyerp.utils import TinyDict

import tinyerp.widgets as tw

_VIEW_MODELS = {'global': 'ir.ui.view',
                'user': 'ir.ui.view.user'}

class ViewList(controllers.Controller, TinyResource):

    @expose(template="tinyerp.subcontrollers.templates.viewlist")
    def default(self, model, mode='global'):
        
        params = TinyDict()
        params.model = _VIEW_MODELS[mode]
        params.view_mode = ['tree']
        
        params.domain = [('model', '=', model)]
        
        screen = tw.screen.Screen(params, selectable=1)
        screen.widget.pageable = False
        
        return dict(screen=screen, model=model, mode=mode, show_header_footer=False)
    
    @expose()
    def create(self, model, **kw):
        
        view_name = kw.get('name')
        view_type = kw.get('type')
        priority = kw.get('priority', 16)
        
        if not view_name:
            raise redirect('/viewlist', model=model)
        
        arch = """<?xml version="1.0"?>
        <%s string="Unknwown">
            <field name="name"/>
        </%s>
        """ % (view_type, view_type)
        
        proxy = rpc.RPCProxy('ir.ui.view')
        proxy.create(dict(model=model, name=view_name, type=view_type, priority=priority, arch=arch))
        
        raise redirect('/viewlist', model=model)
    
    @expose()
    def copy(self, model, id):
        
        id = int(id)
        
        proxy = rpc.RPCProxy(_VIEW_MODELS['global'])
        data = proxy.read([id])[0]
        
        if data.get('inherit_id'):
            raise redirect('/viewlist', model=model, mode='global')
        
        data.pop('id')
        data['ref_id'] = id
        data['user_id'] = rpc.session.uid
        
        # save the final view (apply all inherited views as well)
        proxy = rpc.RPCProxy(model)
        view_type = data['type']
        res = proxy.fields_view_get(id, view_type)
        data['arch'] = res['arch']
        
        proxy = rpc.RPCProxy(_VIEW_MODELS['user'])
        proxy.create(data)

        raise redirect('/viewlist', model=model, mode='user')
        
    @expose()
    def delete(self, model, id, mode='global'):
        
        id = int(id)
        
        proxy = rpc.RPCProxy(_VIEW_MODELS[mode])
        proxy.unlink(id)
        
        raise redirect('/viewlist', model=model, mode=mode)
