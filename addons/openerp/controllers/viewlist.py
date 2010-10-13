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
# -   All names, links and logos of Tiny, OpenERP and Axelor must be
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
from openerp.controllers import SecuredController
from openerp.utils import rpc, TinyDict
from openerp.widgets.screen import Screen

from openobject.tools import expose, redirect


class ViewList(SecuredController):

    _cp_path = "/openerp/viewlist"

    @expose(template="/openerp/controllers/templates/viewlist.mako")
    def index(self, model):

        params = TinyDict()
        params.model = 'ir.ui.view'
        params.view_mode = ['tree']

        params.domain = [('model', '=', model)]

        screen = Screen(params, selectable=1)
        screen.widget.pageable = False

        return dict(screen=screen, model=model)

    @expose()
    def create(self, model, **kw):

        view_name = kw.get('name')
        view_type = kw.get('type')
        priority = kw.get('priority', 16)

        if not view_name:
            raise redirect('/openerp/viewlist', model=model)

        proxy = rpc.RPCProxy(model)
        fields = proxy.fields_get({}).keys()
        string = "Unknown"

        try:
            proxy2 = rpc.RPCProxy('ir.model')
            mid = proxy2.search([('model','=',model)])[0]
            string = proxy2.read([mid], ['name'])[0]['name']
        except:
            pass

        fname = None
        for n in ('name', 'x_name'):
            if n in fields:
                fname = n
                break

        if fname:
            arch = """<?xml version="1.0"?>
            <%s string="%s">
                <field name="%s"/>
            </%s>
            """ % (view_type, string, fname, view_type)

            proxy = rpc.RPCProxy('ir.ui.view')
            proxy.create(dict(model=model, name=view_name, type=view_type, priority=priority, arch=arch))

        raise redirect('/openerp/viewlist', model=model)

    @expose()
    def delete(self, model, id):

        id = int(id)

        proxy = rpc.RPCProxy('ir.ui.view')
        proxy.unlink(id)

        raise redirect('/openerp/viewlist', model=model)

# vim: ts=4 sts=4 sw=4 si et
