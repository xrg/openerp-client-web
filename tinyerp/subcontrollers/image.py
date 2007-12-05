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

import base64

from turbogears import expose
from turbogears import redirect
from turbogears import controllers

from tinyerp import rpc
from tinyerp.tinyres import TinyResource

class Image(controllers.Controller, TinyResource):

    @expose(template="tinyerp.subcontrollers.templates.image")
    def index(self, **kw):
       
        saved = kw.get('saved') or None
        model = kw.get('model')
        id = kw.get('id')
        field = kw.get('field')

        return dict(model=model, saved=saved, id=id, field=field, show_header_footer=False)

    @expose(content_type='application/octet')
    def get_image(self, **kw):
        model = kw.get('model')
        field = kw.get('field')
        id = kw.get('id')

        proxy = rpc.RPCProxy(model)
        res = proxy.read([id], [field])[0]

        res = res.get(field)

        return base64.decodestring(res)

    @expose(template="tinyerp.subcontrollers.templates.image")
    def add(self, upimage,  **kw):

        saved = kw.get('saved') or None
        
        datas = upimage.file.read()

        model = kw.get('model')
        id = int(kw.get('id'))
        field = kw.get('field')

        value = base64.encodestring(datas)

        data = {field: value}

        proxy = rpc.RPCProxy(model)
        res = proxy.write([id], data)
        
        if res:
            saved = 1
        
        return dict(model=model, saved=saved, id=id, field=field, show_header_footer=False)

    @expose(template="tinyerp.subcontrollers.templates.image")
    def delete(self, **kw):

        saved = None
        model = kw.get('model')
        id = int(kw.get('id'))
        field = kw.get('field')

        proxy = rpc.RPCProxy(model)
        proxy.write([id], {field: False})

        return dict(model=model, saved=saved, id=id, field=field, show_header_footer=False)

    @expose(content_type='application/octet')
    def save_as(self, **kw):

        model = kw.get('model')
        id = int(kw.get('id'))
        field = kw.get('field')

        proxy = rpc.RPCProxy(model)
        res = proxy.read([id], [field])[0]

        res = res.get(field)
        
        if not res:
            raise redirect('/image', **kw)
        
        return base64.decodestring(res)
