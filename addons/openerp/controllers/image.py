###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# The OpenERP web client is distributed under the "OpenERP Public License".
# It's based on Mozilla Public License Version (MPL) 1.1 with following
# restrictions:
#
# -   All names, links and logos of Tiny, Open ERP and Axelor must be
#     kept as in original distribution without any changes in all software
#     screens, especially in start-up page and the software header, even if
#     the application source code has been changed or updated or code has been
#     added.
#
# -   All distributions of the software must keep source code with OEPL.
#
# -   All integrations to any other software must keep source code with OEPL.
#
# If you need commercial licence to remove this kind of restriction please
# contact us.
#
# You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################
import base64

import cherrypy
from openerp.controllers import SecuredController
from openerp.utils import rpc
from openerp.widgets.form import get_temp_file

from openobject.tools import expose, redirect


class Image(SecuredController):

    _cp_path = "/openerp/image"

    @expose(template="templates/image.mako")
    def index(self, **kw):

        saved = kw.get('saved') or None
        model = kw.get('model')
        id = kw.get('id')
        field = kw.get('field')

        return dict(model=model, saved=saved, id=id, field=field)

    @expose(content_type='application/octet')
    def get_image(self, **kw):
        model = kw.get('model')
        field = kw.get('field')
        id = int(kw.get('id'))

        proxy = rpc.RPCProxy(model)
        res = proxy.read([id], [field])[0]
        res = res.get(field)

        if res:
            return base64.decodestring(res)
        else:
            return ''

    @expose(content_type='application/octet')
    def get_picture(self, **kw):
        fname = get_temp_file(**kw)
        data = open(fname).read()
        if not data:
            # empty file that have just been created by get_temp_file
            raise cherrypy.HTTPError(404)
        return data

    @expose(template="templates/image.mako")
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

        return dict(model=model, saved=saved, id=id, field=field)

    @expose(template="templates/image.mako")
    def delete(self, **kw):

        saved = None
        model = kw.get('model')
        id = int(kw.get('id'))
        field = kw.get('field')

        proxy = rpc.RPCProxy(model)
        proxy.write([id], {field: False})

        return dict(model=model, saved=saved, id=id, field=field)

    @expose(content_type='application/octet')
    def save_as(self, **kw):

        model = kw.get('model')
        id = int(kw.get('id'))
        field = kw.get('field')

        proxy = rpc.RPCProxy(model)
        res = proxy.read([id], [field])[0]

        res = res.get(field)

        if not res:
            raise redirect('/openerp/image', **kw)

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

