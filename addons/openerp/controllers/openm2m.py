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
import cherrypy
from openerp.utils import rpc, TinyDict, context_with_concurrency_info
from openerp.widgets.form import Hidden

from form import Form, get_validation_schema, default_error_handler, default_exception_handler
from openobject.tools import expose, validate, error_handler, exception_handler


class OpenM2M(Form):

    _cp_path = "/openerp/openm2m"

    @expose(template="templates/openm2m.mako")
    def create(self, params, tg_errors=None):

        params.m2m = params.m2m or params.source
        params.editable = params.get('_terp_editable', True)
        params.hidden_fields = [Hidden(name='_terp_m2m', default=params.m2m)]
        form = self.create_form(params, tg_errors)

        return dict(form=form, params=params)

    @expose()
    @validate(form=get_validation_schema)
    @error_handler(default_error_handler)
    @exception_handler(default_exception_handler)
    def save(self, terp_save_only=False, **kw):
        params, data = TinyDict.split(kw)

        # remember the current page (tab) of notebooks
        cherrypy.session['remember_notebooks'] = True

        # bypass save, for button action in non-editable view
        if not (params.button and not params.editable and params.id):

            proxy = rpc.RPCProxy(params.model)

            if not params.id:
                id = proxy.create(data, params.context)
                params.ids = (params.ids or []) + [int(id)]
                params.id = int(id)
                params.count += 1
            else:
                ctx = context_with_concurrency_info(params.context, params.concurrency_info)
                id = proxy.write([params.id], data, ctx)

        current = params.chain_get(params.source or '')
        button = (params.button or False) and True

        params.load_counter = 1
        if current and current.id and not button:
            params.load_counter = 2

        # perform button action
        if params.button:
            res = self.button_action(params)
            if res:
                return res


        if current:
            current.id = None
            if not params.id:
                params.id = int(id)
        elif not button:
            params.editable = False

        if not current and not button:
            params.load_counter = 2

        return self.create(params)

    @expose()
    def new(self, **kw):
        params, data = TinyDict.split(kw)

        if not params.model:
            params.update(kw)

        params.view_mode = ['form', 'tree']
        params.view_type = 'form'

        params.editable = params.get('_terp_editable', True)

        return self.create(params)
