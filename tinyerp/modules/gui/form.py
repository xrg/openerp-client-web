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

"""
This module implementes view for a tiny model having

    view_type = 'form'
    view_mode = 'form,tree'

@todo: show validation errors
"""

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
    def create(self, model, id=None, ids=[], state='', view_ids=[], view_mode=['form', 'tree'], view_mode2=['tree', 'form'], domain=[], context={}, tg_errors=None, **kw):
        """Create form view...

        @param model: the model
        @param id: current record id
        @param ids: all record ids
        @param state: workflow state?
        @param view_ids: view ids
        @param view_mode: view mode
        @param view_mode2: the original view mode
        @param domain: the domain
        @param context: the context

        @todo: maintain states

        @return: form view
        """

        if tg_errors:
            form = cherrypy.request.terp_form
        else:
            form = tw.form_view.ViewForm(model=model, state=state, id=id, ids=ids, view_ids=view_ids, view_mode=view_mode, view_mode2=view_mode2, domain=domain, context=context)

        return dict(form=form)

    @expose()
    def new(self, **kw):
        terp, data = TinyDict.split(kw)

        if terp.id or terp.ids:
            terp.id = None

        if terp.view_mode[0] == 'tree':
            terp.view_mode.reverse()

        return self.create(**terp)

    @expose()
    def edit(self, **kw):
        terp, data = TinyDict.split(kw)

        if terp.view_mode[0] == 'tree':
            terp.view_mode.reverse()

        return self.create(**terp)

    def get_form(self):
        terp, data = TinyDict.split(cherrypy.request.params)

        cherrypy.request.terp_validators = {}

        form = tw.form_view.ViewForm(**terp)
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
        terp, data = TinyDict.split(kw)

        if tg_errors:
            return self.create(tg_errors=tg_errors, **terp)

        proxy = rpc.RPCProxy(terp.model)

        if not terp.id:
            res = proxy.create(data, terp.context)
            terp.ids = (terp.ids or []) + [int(res)]
        else:
            res = proxy.write([terp.id], data, terp.context)

        return self.create(**terp)

    @expose()
    def delete(self, **kw):
        terp, data = TinyDict.split(kw)

        proxy = rpc.RPCProxy(terp.model)

        idx = -1
        if terp.id:
            res = proxy.unlink([terp.id])
            idx = terp.ids.index(terp.id)
            terp.ids.remove(terp.id)

            if idx == len(terp.ids):
                idx = -1

        terp.id = (terp.ids or None) and terp.ids[idx]

        return self.create(**terp)

    @expose()
    def prev(self, **kw):
        terp, data = TinyDict.split(kw)
        idx = -1

        if terp.id:
            idx = terp.ids.index(terp.id)
            idx = idx-1

            if idx == terp.ids[0]:
                idx = len(terp.ids)
                terp.id = terp.ids[idx]

        if terp.ids:
            terp.id = terp.ids[idx]

        return self.create(**terp)

    @expose()
    def next(self, **kw):
        terp, data = TinyDict.split(kw)
        idx = 0

        if terp.id:
            idx = terp.ids.index(terp.id)
            idx = idx + 1

            if idx == len(terp.ids):
                idx = 0

        if terp.ids:
            terp.id = terp.ids[idx]

        return self.create(**terp)

    @expose()
    def find(self, **kw):
        terp, data = TinyDict.split(kw)

        terp.ids = []

        search_window = search.Search()
        return search_window.create(**terp)

    @expose()
    def switch(self, **kw):
        terp, data = TinyDict.split(kw)

        terp.view_mode.reverse()

        terp.ids = terp.ids or []
        if terp.ids:
            terp.id = terp.ids[0]

        return self.create(**terp)

    @expose()
    def search_M2O(self, model, textid, hiddenname, s_domain, **kw):
        search_window = search.Search()
        return search_window.create(model=model, textid=textid, hiddenname=hiddenname, s_domain=s_domain)
