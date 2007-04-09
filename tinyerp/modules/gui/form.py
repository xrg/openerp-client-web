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

from tinyerp import tools
from tinyerp import widgets as tw
from tinyerp.tinyres import TinyResource
from tinyerp.modules.utils import TinyDict

import search

class Form(controllers.Controller, TinyResource):

    @expose(template="tinyerp.modules.gui.templates.form")
    def create(self, params, tg_errors=None):

        if tg_errors:
            form = cherrypy.request.terp_form
        else:
            form = tw.form_view.ViewForm(params)

        return dict(form=form)

    @expose()
    def new(self, **kw):
        params, data = TinyDict.split(kw)

        if params.id or params.ids:
            params.id = None

        if params.view_mode[0] == 'tree':
            params.view_mode.reverse()

        return self.create(params)

    @expose()
    def edit(self, **kw):
        params, data = TinyDict.split(kw)

        current = params[params.one2many or ''] or params

        if current.view_mode[0] == 'tree':
            current.view_mode.reverse()

        return self.create(params)

    def get_form(self):
        params, data = TinyDict.split(cherrypy.request.params)

        cherrypy.request.terp_validators = {}

        form = tw.form_view.ViewForm(params)
        cherrypy.request.terp_form = form

        vals = cherrypy.request.terp_validators
        schema = validators.Schema(**vals)

        form.validator = schema

        return form

    @expose()
    @validate(form=get_form)
    def save(self, tg_errors=None, tg_source=None, tg_exceptions=None, **kw):
        """Controller method to save current record.

        @param kw: keyword arguments

        @todo: validate params
        @todo: error_handler

        @return: form view
        """
        params, data = TinyDict.split(kw)

        if tg_errors:
            return self.create(params, tg_errors=tg_errors)

        proxy = rpc.RPCProxy(params.model)

        if not params.id:
            res = proxy.create(data, params.context)
            params.ids = (params.ids or []) + [int(res)]
        else:
            res = proxy.write([params.id], data, params.context)


        current = params[params.one2many or '']
        if current:
            current.id = None
            if current.view_mode[0] == 'tree':
                current.view_mode.reverse()

        return self.create(params)

    @expose()
    def delete(self, **kw):
        params, data = TinyDict.split(kw)

        current = params[params.one2many or ''] or params

        proxy = rpc.RPCProxy(current.model)

        idx = -1
        if current.id:
            res = proxy.unlink([current.id])
            idx = current.ids.index(current.id)
            current.ids.remove(current.id)

            if idx == len(current.ids):
                idx = -1

        current.id = (current.ids or None) and current.ids[idx]

        return self.create(params)

    @expose()
    def prev(self, **kw):
        params, data = TinyDict.split(kw)

        current = params[params.one2many or ''] or params

        idx = -1

        if current.id:
            idx = current.ids.index(current.id)
            idx = idx-1

            if idx == current.ids[0]:
                idx = len(current.ids)
                current.id = current.ids[idx]

        if current.ids:
            current.id = current.ids[idx]

        return self.create(params)

    @expose()
    def next(self, **kw):
        params, data = TinyDict.split(kw)

        current = params[params.one2many or ''] or params

        idx = 0

        if current.id:
            idx = current.ids.index(current.id)
            idx = idx + 1

            if idx == len(current.ids):
                idx = 0

        if current.ids:
            current.id = current.ids[idx]

        return self.create(params)

    @expose()
    def find(self, **kw):
        params, data = TinyDict.split(kw)

        params.found_ids = []

        search_window = search.Search()
        return search_window.create(params)

    @expose()
    def switch(self, **kw):

        # get special _terp_ params and data
        params, data = TinyDict.split(kw)

        # select the right params field (if one2many toolbar button)
        current = params[params.one2many or ''] or params

        # switch the view mode
        current.view_mode.reverse()

        # set ids and id
        current.ids = current.ids or []
        if current.ids:
            current.id = current.ids[0]

        # regenerate the view
        return self.create(params)

