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

from turbogears import expose
from turbogears import controllers

from tinyerp import rpc

from tinyerp.tinyres import TinyResource

from tinyerp.modules.utils import TinyDict
from tinyerp.modules.utils import TinyForm
from tinyerp.modules.utils import TinyFormError

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
            frm = TinyForm('form', 'kind', **kw)
            
            data = {}
            if model != params.model:
               
                fld = frm.keys()[0]
                data = {fld : [(id and 1, id, frm[fld].copy())]}
                
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
    def get(self, **kw):
        params, data = TinyDict.split(kw)

        params.ids = None
        params.domain = []

        params.view_mode = ['form', 'tree']
        if params.source == '_terp_list':
            params.view_mode = ['tree', 'form']
        
        frm = form.Form().create_form(params)

        wid = frm.screen.get_widgets_by_name(params.source)[0]
        ids = []
        
        if params.source != '_terp_list':
            wid = wid.screen.widget
            proxy = rpc.RPCProxy(params.model)
            ids = proxy.read([params.id], [params.source])[0][params.source]
        else:
            ids = wid.ids

        if params.edit_inline:
            wid.edit_inline = params.edit_inline

        return dict(ids=str(ids), view=ustr(wid.render()))
