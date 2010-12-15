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
import urllib

import cherrypy
from openerp import widgets as tw
from openerp.utils import rpc, TinyDict, context_with_concurrency_info

from form import Form, get_validation_schema, default_error_handler, default_exception_handler
from openobject.tools import expose, validate, error_handler, exception_handler


class OpenO2M(Form):

    _cp_path = "/openerp/openo2m"

    def create_form(self, params, tg_errors=None):

        params.id = params.o2m_id
        params.model = params.o2m_model
        params.view_mode = ['form', 'tree']
        params.view_type = 'form'

        #XXX: dirty hack to fix bug #401700
        if not params.get('_terp_view_ids'):
            params['_terp_view_ids'] = []

        # to get proper view, first generate form using the view_params
        vp = params.view_params

        form = tw.form_view.ViewForm(vp, name="view_form", action="/openerp/openo2m/save")
        cherrypy.request.terp_validators = {}
        wid = form.screen.widget.get_widgets_by_name(params.o2m)[0]

        # save view_params for later phazes
        vp = vp.make_plain('_terp_view_params/')
        hiddens = map(lambda x: tw.form.Hidden(name=x, default=ustr(vp[x])), vp)

        params.prefix = params.o2m
        params.views = wid.view

        ctx = params.context or {}
        ctx.update(params.parent_context or {})
        ctx.update(params.o2m_context or {})
        p, ctx = TinyDict.split(ctx)
        if ctx.get('default_name'):
            del ctx['default_name']
        params.context = ctx or {}
        params.hidden_fields = [tw.form.Hidden(name='_terp_parent_model', default=params.parent_model),
                                tw.form.Hidden(name='_terp_parent_id', default=params.parent_id),
                                tw.form.Hidden(name='_terp_parent_context', default=ustr(params.parent_context)),
                                tw.form.Hidden(name='_terp_o2m', default=params.o2m),
                                tw.form.Hidden(name='_terp_o2m_id', default=params.id or None),
                                tw.form.Hidden(name='_terp_o2m_model', default=params.o2m_model),
                                tw.form.Hidden(name='_terp_o2m_context', default=ustr(params.o2m_context or {})),
                                tw.form.Hidden(name=params.prefix + '/__id', default=params.id or None)] + hiddens

        form = tw.form_view.ViewForm(params, name="view_form", action="/openerp/openo2m/save")
        form.screen.string = wid.screen.string

        return form

    @expose(template="/openerp/controllers/templates/openo2m.mako")
    def create(self, params, tg_errors=None):

        if tg_errors:
            form = cherrypy.request.terp_form
        else:
            form = self.create_form(params, tg_errors)

        return dict(form=form, params=params)

    @expose()
    @validate(form=get_validation_schema)
    @error_handler(default_error_handler)
    @exception_handler(default_exception_handler)
    def save(self, terp_save_only=False, **kw):
        params, data = TinyDict.split(kw)
        params.editable = True

        proxy = rpc.RPCProxy(params.parent_model)

        pprefix = '.'.join(params.o2m.split('/')[:-1])

        if pprefix:
            data = eval(pprefix, TinyDict(**data)).make_dict()

        ctx = context_with_concurrency_info(rpc.session.context, params.concurrency_info)
        ctx.update(params.parent_context or {})
        ctx.update(params.o2m_context or {})

        id = proxy.write([params.parent_id], data, ctx)

        prefix = params.o2m
        current = params.chain_get(prefix)

        params.load_counter = 1

        ids = current.ids
        fld = params.o2m.split('/')[-1]
        all_ids = proxy.read([params.parent_id], [fld])[0][fld]
        new_ids = [i for i in all_ids if i not in ids]

        current.ids = all_ids
        if new_ids and params.source:
            current.id = new_ids[-1]
            params.o2m_id = current.id

        # perform button action
        if params.button:
            current.button = params.button
            current.parent_params = params
            cherrypy.request._terp_view_target = 'new'
            res = self.button_action(current)
            if res:
                return res

        return self.create(params)

    @expose()
    def edit(self, **kw):
        params, data = TinyDict.split(kw)
        return self.create(params)
    
    @expose('json', methods=('POST',))
    def delete(self, model, id):
        error = False
        res=""
        proxy = rpc.RPCProxy(model)
        try:
            if id:
                res  = proxy.unlink([id])
        except Exception, e:
            error = ustr(e)
            
        return dict(error=error)

# vim: ts=4 sts=4 sw=4 si et
