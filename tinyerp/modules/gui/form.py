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
"""

from turbogears import expose
from turbogears import widgets
from turbogears import controllers

import cherrypy

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp import tools
from tinyerp import widgets as tw
from tinyerp.tinyres import TinyResource

import search

def make_dict(data):
    """Generates a valid dictionary from the given data to be used with TinyERP.
    """
    res = {}
    for name, value in data.items():
        names = name.split('/')

        if len(names) > 1:
            res.setdefault(names[0], {}).update({"/".join(names[1:]): value})
        else:
            res[name] = value or False

    for k, v in res.items():
        if type(v) == type({}):
            #res[k] = make_dict(v)

            id = 0
            if '__id' in v:
                id = int(v.pop('__id'))

            res[k] = [(id and 1, id, make_dict(v))]

    return res

class Form(controllers.Controller, TinyResource):

    def __init__(self):
        pass

    @staticmethod
    def create(model, id=None, ids=[], view_ids=[], view_mode=['form', 'tree'], domain=[], context={}):
        """Create a new instance of form.

        @param model: the model
        @param id: current record id
        @param ids: all record ids
        @param view_ids: view ids
        @param view_mode: view mode
        @param domain: the domain
        @param context: the context
        """

        form = Form()

        form.proxy = rpc.RPCProxy(model)
        form.model = model
        form.view_ids = view_ids
        form.view_mode = view_mode
        form.domain = domain
        form.context = context
        form.state = '' #TODO: maintain states

        form.id = id
        form.ids = ids

        return form

    @expose(template="tinyerp.modules.gui.templates.form")
    def view(self):

        self.screen = tw.screen.Screen(prefix='',
                                       model=self.model,
                                       id=self.id,
                                       ids=self.ids,
                                       view_ids=self.view_ids,
                                       view_mode=self.view_mode,
                                       domain=self.domain,
                                       context=self.context)

        self.ids = self.screen.ids
        cherrypy.session['_terp_ids'] = self.ids

        return dict(screen=self.screen,
                    model=self.model,
                    id=self.id,
                    ids=self.ids,
                    view_ids=self.view_ids,
                    view_mode=self.view_mode,
                    domain=self.domain,
                    context=self.context,
                    state=self.state)

    def new(self):
        if self.id or self.ids:
            self.id = None

    def save(self, data={}):

        if not self.id:
            res = self.proxy.create(data, self.context)
            self.ids = (self.ids or []) + [int(res)]
        else:
            res = self.proxy.write([self.id], data, self.context)

    def prev(self):
        idx = 0
        if self.id:
            idx = self.ids.index(self.id)
            idx = idx-1

            if idx == self.ids[0]:
                idx = len(self.ids)
                self.id = self.ids[idx]

            if self.ids:
                self.id = self.ids[idx]

    def next(self):
        idx = 0
        if self.id:
            idx = self.ids.index(self.id)
            idx = idx + 1

            if idx == len(self.ids):
                idx = 0

            if self.ids:
                self.id = self.ids[idx]

    def delete(self):
        idx = -1
        if self.id:
            res = self.proxy.unlink([self.id])
            idx = self.ids.index(self.id)
            self.ids.remove(self.id)

            if idx == len(self.ids):
                idx = -1

        if self.ids:
            self.id = self.ids[idx]

        else:
            self.id = None

        #self.id = (self.ids or None) and self.ids[0]

    @expose()
    def action(self, _terp_model,
                     _terp_id=None,
                     _terp_domain=[],
                     _terp_view_ids=[],
                     _terp_view_mode=['form', 'tree'],
                     _terp_context={},
                     _terp_action="save",
                     _terp_state=None,
                     **data):
        """Form action controller, performs either of the 'new', 'save',
        'delete', 'edit', 'search', 'button' actions.

        @param _terp_model: the mode
        @param _terp_id: current record id
        @param _terp_domain: the domain
        @param _terp_view_ids: view ids
        @param _terp_view_mode: the view mode
        @param _terp_context: the local context
        @param _terp_action: the action
        @param _terp_state: the state
        @param data: the data

        @return: view of the form or search controller
        """

        action = _terp_action
        model = _terp_model
        state = _terp_state

        #cherrypy.session['open'] = True

        id = (_terp_id or None) and eval(_terp_id)
        ids = cherrypy.session.get('_terp_ids', [])

        domain = (_terp_domain or []) and eval(_terp_domain)
        context = (_terp_context or {}) and eval(_terp_context)
        view_ids = (_terp_view_ids or []) and eval(_terp_view_ids)
        view_mode = (_terp_view_mode or ['form', 'tree']) and eval(_terp_view_mode)

        if action == 'search':
            search_window = search.Search.create(model, [], view_ids, domain, context)
            return search_window.view()

        if action == 'switch':
            view_mode.reverse()

            if view_mode[0] == 'tree':
                view_ids = [False] + view_ids
            else:
                if False in view_ids: view_ids.remove(False)

            ids = ids or []
            if ids:
                id = ids[0]

        if action == 'new' and view_mode[0] == 'tree':
            view_mode.reverse()

        if action == 'edit':
            view_mode = ['form', 'tree']

        form = Form.create(model=model,
                           id=id,
                           ids=ids,
                           view_ids=view_ids,
                           view_mode=view_mode,
                           domain=domain,
                           context=context)

        if action == 'new':
            form.new()

        elif action == 'save':
            form.save(make_dict(data))

        elif action == 'delete':
            form.delete()

        elif action == 'edit':
            #TODO: open record
            pass

        elif action == 'prev':
            form.prev()

        elif action == 'next':
            form.next()

        elif action == 'button':
            #TODO: perform button action
            pass

        return form.view()
