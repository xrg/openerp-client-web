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

import base64

from turbogears import expose
from turbogears import redirect
from turbogears import controllers
import cherrypy

from openerp import rpc
from openerp.tinyres import TinyResource

class Image(controllers.Controller, TinyResource):

    @expose(template="openerp.subcontrollers.templates.image")
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

    @expose(template="openerp.subcontrollers.templates.image")
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

    @expose(template="openerp.subcontrollers.templates.image")
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

    @expose()
    def b64(self, **kw):
        #idea from http://dean.edwards.name/weblog/2005/06/base64-ie/
        try:
            qs = cherrypy.request.query_string
            content_type, data = qs.split(';')
            data_type, data = data.split(',')
            assert(data_type == 'base64')
            cherrypy.response.headers['Content-Type'] = content_type
            return base64.decodestring(data)
        except:
            raise cherrypy.HTTPError(400)   # Bad request

# vim: ts=4 sts=4 sw=4 si et

