###############################################################################
#
# Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id: shortcuts.py 334 2007-05-11 13:22:31Z ame $
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

from turbogears import expose
from turbogears import redirect
from turbogears import controllers

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp.tinyres import TinyResource

class Requests(controllers.Controller, TinyResource):
    
    def my(self):

        if not rpc.session.is_logged():
            return [],[]

        proxy = rpc.RPCProxy('res.request')
        ids, ids2 = proxy.request_get()
        
        msg = "No request"
        if len(ids):
            msg = '%s request(s)' % len(ids)
            
        if len(ids2):
            msg += ' - %s pending request(s)' % len(ids2)

        return ids, msg
    
    @expose()
    def default(self, ids):
        from tinyerp.modules import actions
        ids = eval(ids)
        return actions._execute_window(False, 'res.request', res_id=ids, domain=[('act_to','=',rpc.session.uid)], view_type='form', mode='tree,form')
