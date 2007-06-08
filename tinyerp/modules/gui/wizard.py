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
from tinyerp.modules.utils import TinyDict

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
            action = model.replace('wizard.', '')
        else:
            model = 'wizard.' + action

        params.name = action
        params.model = model
        params.view_mode = []

        if 'form' not in datas:
            datas['form'] = {}

        wiz_id = rpc.session.execute('wizard', 'create', action)

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
                res['datas'].update(datas['form'])
                form.screen.add_view(res)

                # store datas in _terp_datas
                form.hidden_fields = [
                                      widgets.HiddenField(name='_terp_datas', default=str(datas)),
                                      widgets.HiddenField(name='_terp_state2', default=state)
                                  ]

                buttons = res.get('state', [])
                if hasattr(cherrypy.request, 'terp_form'):
                    cherrypy.request.terp_buttons = buttons

                params.state = state
                return dict(form=form, buttons=buttons)

            elif res['type']=='action':
                from tinyerp.modules import actions

                dmodel = datas['model']
                did = datas['id']

                if res['action']:
                    return actions._execute(res['action'], **datas)
                else:
                    raise redirect('/tree/open?model=%s&id=%s'%(dmodel,did))

            elif res['type']=='print':
                from tinyerp.modules import actions

                datas['report_id'] = res.get('report_id', False)
                if res.get('get_id_from_action', False):
                    backup_ids = datas['ids']
                    datas['ids'] = datas['form']['ids']

                return actions._execute_report(res['report'], **datas)

            elif res['type']=='state':
                state = res['state']

        raise redirect('/wizard/end')

    @expose(template="tinyerp.modules.gui.templates.wizard")
    def create(self, params, tg_errors=None):

        if tg_errors:
            form = cherrypy.request.terp_form
            buttons = cherrypy.request.terp_buttons
            return dict(form=form, buttons=buttons)

        return self.execute(params)

    @expose()
    def end(self, **kw):
        raise redirect('/')

    def get_form(self):
        params, datas = TinyDict.split(cherrypy.request.params)
        #params.datas['form'].update(datas)

        params.state = params.state2

        cherrypy.request.terp_validators = {}

        form = self.execute(params)['form']
        cherrypy.request.terp_form = form

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
    def action(self, tg_errors=None, tg_source=None, tg_exceptions=None, **kw):
        params, datas = TinyDict.split(kw)
        params.datas['form'].update(datas)

        return self.create(params, tg_errors=tg_errors)
