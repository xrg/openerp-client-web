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
from turbogears import redirect
from turbogears import controllers

import cherrypy

from openerp import rpc
from openerp import tools
from openerp import common

from openerp.tinyres import TinyResource

class Requests(controllers.Controller, TinyResource):
    
    def my(self):

        if not rpc.session.is_logged():
            return [],[]
        
        ids, ids2 = cherrypy.session.get('terp_requests', (False, False))
        if ids == False:
            ids, ids2 = rpc.RPCProxy('res.request').request_get()
            cherrypy.session['terp_requests'] = (ids, ids2)

        msg = _("No request")
        if len(ids):
            msg = _('%s request(s)') % len(ids)
            
        if len(ids2):
            msg += _(' - %s pending request(s)') % len(ids2)

        return ids, msg
    
    @expose()
    def default(self, ids):
        from openerp.subcontrollers import actions
        #ids = eval(ids)
        
        #read requests
        ids, ids2 = rpc.RPCProxy('res.request').request_get()

        return actions.execute_window(False, 'res.request', res_id=None, domain=[('act_to','=',rpc.session.uid)], view_type='form', mode='tree,form')

# vim: ts=4 sts=4 sw=4 si et

