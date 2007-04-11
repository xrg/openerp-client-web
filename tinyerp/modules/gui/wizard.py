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

    @expose(template="tinyerp.modules.gui.templates.wizard")
    def create(self, params, tg_errors=None):

        if tg_errors:
            return dict(form = cherrypy.request.terp_form)

        params.model = "wizard."+params.name
        params.view_mode = []

        form = tw.form_view.ViewForm(params, name="view_form", action="/wizard/action")

        wiz_id = rpc.session.execute('/wizard', 'create', params.name)
        res = rpc.session.execute('/wizard', 'execute', wiz_id, params.data, params.state, rpc.session.context)

        form.screen.add_view(res)

        return dict(form=form, states=res.get('state', []))

    @expose()
    def action(self, state, **kw):
        # TODO: Perform wizard action
        return dict()
