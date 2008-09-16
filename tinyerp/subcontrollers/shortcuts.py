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
from turbogears import redirect
from turbogears import controllers

import cherrypy

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp.tinyres import TinyResource

class Shortcuts(controllers.Controller, TinyResource):

    def my(self):

        if not rpc.session.is_logged():
            return []
        
        sc = cherrypy.session.get('terp_shortcuts', False)
        if not sc:
            proxy = rpc.RPCProxy('ir.ui.view_sc')
            sc = proxy.get_sc(rpc.session.uid, 'ir.ui.menu', rpc.session.context) or []
            
            cherrypy.session['terp_shortcuts'] = sc
            
        for x in sc:
            if isinstance(x['res_id'], (list, tuple)):
                x['res_id'] = x['res_id'][0]

        return sc
    
    def can_create(self):
        return (rpc.session.is_logged() and 
                rpc.session.active_id and 
                cherrypy.request.path == '/tree/open' and 
                cherrypy.request.params.get('model') == 'ir.ui.menu')

    @expose()
    def default(self):
        from tinyerp.subcontrollers import actions

        domain = [('user_id', '=', rpc.session.uid), ('resource', '=', 'ir.ui.menu')]
        return actions.execute_window(False, 'ir.ui.view_sc', res_id=None, domain=domain, view_type='form', mode='tree,form')

    @expose()
    def add(self, id):
        id = int(id)
        proxy = rpc.RPCProxy('ir.ui.view_sc')
        
        sc = cherrypy.session.get('terp_shortcuts', False)
        
        if sc:
            for s in sc:
                if s['res_id'] == id:
                    raise redirect('/tree/open', id=id, model='ir.ui.menu')

        name = rpc.RPCProxy('ir.ui.menu').name_get([id], rpc.session.context)[0][1]
        proxy.create({'user_id': rpc.session.uid, 'res_id': id, 'resource': 'ir.ui.menu', 'name': name})

        sc = proxy.get_sc(rpc.session.uid, 'ir.ui.menu', rpc.session.context)
        cherrypy.session['terp_shortcuts'] = sc

        raise redirect('/tree/open', id=id, model='ir.ui.menu')
        
# vim: ts=4 sts=4 sw=4 si et

