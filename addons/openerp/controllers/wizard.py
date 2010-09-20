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
import re

import cherrypy
from openerp import widgets as tw, validators
from openerp.controllers import SecuredController
from openerp.utils import rpc, icons, TinyDict

import form
from openobject.tools import expose, redirect, validate, error_handler
from openobject import pooler
import openobject

class Wizard(SecuredController):

    _cp_path = "/openerp/wizard"

    def execute(self, params):

        action = params.name
        model = params.model
        state = params.state
        datas = params.datas

        form = None
        buttons = []

        if model:
            action = model.replace('wizard.', '', 1)
        else:
            model = 'wizard.' + action

        params.name = action
        params.model = model
        params.view_mode = []

        if 'form' not in datas:
            datas['form'] = {}

        wiz_id = params.wiz_id or rpc.session.execute('wizard', 'create', action)

        while state != 'end':

            ctx = rpc.session.context.copy()
            ctx.update(datas.get('context' or {}) or {})

            res = rpc.session.execute('wizard', 'execute', wiz_id, datas, state, ctx)

            if 'datas' in res:
                datas['form'].update(res['datas'])
            else:
                res['datas'] = {}

            if res['type']=='form':

                fields = res['fields']
                form_values = {}

                for f in fields:
                    if 'value' in fields[f]:
                        form_values[f] = fields[f]['value']
                    
                    if f in datas['form'] and fields[f]['type'] == "one2many":
                        datas['form'][f] = [(1, d, {}) for d in datas['form'][f]]

                form_values.update(datas['form'])

                datas['form'] = form_values

                res['datas'].update(datas['form'])

                params.is_wizard = True
                params.view_mode = ['form']
                params.view_type = 'form'
                params.views = {'form': res}

                # keep track of datas and some other required information
                params.hidden_fields = [tw.form.Hidden(name='_terp_datas', default=ustr(datas)),
                                        tw.form.Hidden(name='_terp_state2', default=state),
                                        tw.form.Hidden(name='_terp_wiz_id', default=wiz_id)]

                form = tw.form_view.ViewForm(params, name="view_form", action="/openerp/wizard/action")

                buttons = []
                for x in res.get('state', []):
                    x = list(x)
                    x[1] = re.sub('_(?!_)', '', x[1]) # remove mnemonic

                    if len(x) >= 3:
                        x[2] = icons.get_icon(x[2])

                    buttons.append(tuple(x))

                params.state = state
                return dict(form=form, buttons=buttons)

            elif res['type']=='action':
                import actions
                # If configuration is done 
                if res.get('action') and res.get('action').get('res_model') == 'ir.ui.menu' and res['state'] == 'end':
                    return self.end()
                act_res = actions.execute(res['action'], **datas)
                if act_res:
                    return act_res

                state = res['state']

            elif res['type']=='print':
                import actions

                datas['report_id'] = res.get('report_id', False)
                if res.get('get_id_from_action', False):
                    backup_ids = datas['ids']
                    datas['ids'] = datas['form']['ids']

                return actions.execute_report(res['report'], **datas)

            elif res['type']=='state':
                state = res['state']

        raise redirect('/openerp/wizard/end')

    @expose(template="/openerp/controllers/templates/wizard.mako")
    def create(self, params, tg_errors=None):

        if tg_errors:
            form = cherrypy.request.terp_form
            buttons = cherrypy.request.terp_buttons
            return dict(form=form, buttons=buttons)

        return self.execute(params)

    @expose()
    def end(self, **kw):

        if 'wizard_parent_params' in cherrypy.session:
            frm = cherrypy.session['wizard_parent_form']
            params = cherrypy.session['wizard_parent_params']
            try:
                return pooler.get_pool().get_controller(frm).create(params)
            except:
                pass

        import actions
        return actions.close_popup()

    def get_validation_schema(self):

        kw = cherrypy.request.params
        params, datas = TinyDict.split(kw)

        params.state = params.state2

        cherrypy.request.terp_validators = {}

        res = self.execute(params)

        form = res['form']
        buttons = res.get('buttons', [])

        cherrypy.request.terp_form = form
        cherrypy.request.terp_buttons = buttons

        vals = cherrypy.request.terp_validators
        keys = vals.keys()
        for k in keys:
            if k not in kw:
                vals.pop(k)

        form.validator = openobject.validators.Schema(**vals)
        return form

    @expose()
    @validate(form=get_validation_schema)
    @error_handler(form.default_error_handler)
    def report(self, tg_errors=None, tg_exceptions=None, **kw):

        if tg_exceptions:
            raise tg_exceptions

        params, datas = TinyDict.split(kw)
        params.datas['form'].update(datas)

        if tg_errors:
            return self.create(params, tg_errors=tg_errors)

        return self.execute(params)

    @expose()
    @validate(form=get_validation_schema)
    @error_handler(form.default_error_handler)
    def action(self, tg_errors=None, tg_exceptions=None, **kw):

        if tg_exceptions:
            raise tg_exceptions

        params, datas = TinyDict.split(kw)
        params.datas['form'].update(datas)

        return self.create(params, tg_errors=tg_errors)

# vim: ts=4 sts=4 sw=4 si et
