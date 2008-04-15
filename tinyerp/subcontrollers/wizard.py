###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
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
# along with this program; if not, write to the 
# Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
# Boston, MA  02111-1307, USA.
#
###############################################################################

from turbogears import expose
from turbogears import redirect
from turbogears import widgets
from turbogears import controllers
from turbogears import validators
from turbogears import validate
from turbogears import error_handler

import cherrypy

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp import widgets as tw
from tinyerp.tinyres import TinyResource
from tinyerp.utils import TinyDict

import form
import search

class Wizard(controllers.Controller, TinyResource):

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
            ctx.update(params.context or {})

            res = rpc.session.execute('wizard', 'execute', wiz_id, datas, state, ctx)

            if 'datas' in res:
                datas['form'].update(res['datas'])
            else:
                res['datas'] = {}

            if res['type']=='form':
                form = tw.form_view.ViewForm(params, name="view_form", action="/wizard/action")
                
                fields = res['fields']
                form_values = {}
                
                for f in fields:
                    if 'value' in fields[f]:
                        form_values[f] = fields[f]['value']

                form_values.update(datas['form'])
                
                datas['form'] = form_values

                res['datas'].update(datas['form'])
                form.screen.add_view(res)

                # store datas in _terp_datas
                form.hidden_fields = [
                                      widgets.HiddenField(name='_terp_datas', default=ustr(datas)),
                                      widgets.HiddenField(name='_terp_state2', default=state),
                                      widgets.HiddenField(name='_terp_wiz_id', default=wiz_id)
                                  ]

                buttons = res.get('state', [])
                params.state = state
                
                return dict(form=form, buttons=buttons)

            elif res['type']=='action':
                from tinyerp.subcontrollers import actions

                act_res = actions.execute(res['action'], **datas)
                if act_res:
                    return act_res

                state = res['state']

            elif res['type']=='print':
                from tinyerp.subcontrollers import actions
                
                datas['report_id'] = res.get('report_id', False)
                if res.get('get_id_from_action', False):
                    backup_ids = datas['ids']
                    datas['ids'] = datas['form']['ids']

                return actions.execute_report(res['report'], **datas)

            elif res['type']=='state':
                state = res['state']

        raise redirect('/wizard/end')

    @expose(template="tinyerp.subcontrollers.templates.wizard")
    def create(self, params, tg_errors=None):

        if tg_errors:
            form = cherrypy.request.terp_form
            buttons = cherrypy.request.terp_buttons
            return dict(form=form, buttons=buttons)

        return self.execute(params)

    @expose()
    def end(self, **kw):
        
        if 'wizard_parent_form' in cherrypy.session:
            params = cherrypy.session.pop('wizard_parent_form')
            return form.Form().create(params)

        raise redirect('/')

    def get_form(self):
        params, datas = TinyDict.split(cherrypy.request.params)
        #params.datas['form'].update(datas)

        params.state = params.state2

        cherrypy.request.terp_validators = {}

        res = self.execute(params)
        
        form = res['form']
        buttons = res.get('buttons', [])

        cherrypy.request.terp_form = form
        cherrypy.request.terp_buttons = buttons

        vals = cherrypy.request.terp_validators
        schema = validators.Schema(**vals)

        form.validator = schema

        return form

    @expose()
    @validate(form=get_form)
    def report(self, **kw):
        params, datas = TinyDict.split(kw)
        params.datas['form'].update(datas)

        return self.execute(params)

    @expose()
    @validate(form=get_form)
    def action(self, tg_errors=None, **kw):
        params, datas = TinyDict.split(kw)
        params.datas['form'].update(datas)
        
        return self.create(params, tg_errors=tg_errors)
