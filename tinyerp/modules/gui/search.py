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
This module implementes search view for a tiny model. Currently it simply displays
list view of the given model.
"""
import cherrypy

from turbogears import expose
from turbogears import widgets
from turbogears import controllers

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp import tools
from tinyerp import widgets_search as tws
from tinyerp.tinyres import TinyResource

from tinyerp.modules.utils import TinyDict
from tinyerp.modules.utils import TinyParent

import form

def _make_domain(name, type, value):

    if value:

        if type in ('many2many', 'one2many', 'many2one', 'char'):
            return [(name, 'ilike', value)]

        elif type in ('float', 'integer', 'date', 'time', 'datetime'):
            
            start = value.get('from')
            end = value.get('to')            
            
            if start and end:
                return [(name, '>=', start), (name, '<=', end)]
            elif start:
                return [(name, '>=', start)]
            elif end:
                return [(name, '<=', end)]
            return None

        if type=='boolean':
            return [(name, '=', int(value))]

        if  type=='selection':
            return [(name, '=', value)]

    return []

class Search(controllers.Controller, TinyResource):

    @expose(template="tinyerp.modules.gui.templates.search")
    def create(self, params, values={}):
        form = tws.search_view.ViewSearch(params, values=values, name="search_form", action='/search/ok')

        form.form_view.oncancel = self._get_oncancel(params)
        form.form_view.onok = self._get_onok(params)
        form.form_view.onfind = self._get_onfind(params)

        form.javascript = self._get_javascript(params)
        form.form_view.hidden_fields = self._get_hiddenfield(params)
        
        form.list_view.options.on_first = "$('offset').value = 0; %s" % self._get_onfind(params)
        form.list_view.options.on_previous = "$('offset').value = parseInt($('offset').value) - parseInt($('limit').value); %s" % self._get_onfind(params)
        form.list_view.options.on_next = "$('offset').value = parseInt($('offset').value) + parseInt($('limit').value); %s" % self._get_onfind(params)
        
        form.list_view.options.limit = values.get('limit', 20)
        form.list_view.options.offset = values.get('offset', 0)
                        
        return dict(form=form, params=params)

    def _get_oncancel(self, params):
        return "submit_form('/search/cancel')"

    def _get_onok(self, params):
        return "onok('/search/ok', form)"

    def _get_onfind(self, params):
        return "submit_form('/search/find')"

    def _get_javascript(self, params):
        return []

    def _get_hiddenfield(self, params):
        return []

    @expose()
    def ok(self, **kw):
        params, data = TinyDict.split(kw)

        ids = data.get('search_list', [])

        if not isinstance(ids, list):
            ids = [ids]

        if ids:
            params.ids = [int(id) for id in ids]
            params.id = ids[0]

        if params.view_mode[0] == 'tree':
            params.view_mode.reverse() #reverse the mode
            
        params.editable = False # default not-editable view
        return form.Form().create(params)

    @expose()
    def cancel(self, **kw):
        params, data = TinyDict.split(kw)
        
        if params.view_mode[0] == 'tree':
            params.view_mode.reverse() #reverse the mode
            
        return form.Form().create(params)

    @expose()
    def find(self, **kw):
        params, data = TinyDict.split(kw)
        
        fields_type = params.fields_type
        search_domain = []

        # evaluate domain and context for many2many or many2one field
        # XXX: In GTK client this domain is used only in case of no search criteria

        caller = params.get('m2m', params.get('m2o', None))

        if caller:
            ctx = TinyParent(**kw)
            pctx = ctx

            prefix = ''
            if '/' in caller:
                prefix = caller.rsplit('/', 1)[0]
                ctx = ctx[prefix.replace('/', '.')]

            if '/' in prefix:
                prefix = prefix.rsplit('/', 1)[0]
                pctx = pctx[prefix.replace('/', '.')]

            ctx.parent = pctx
            ctx.context = rpc.session.context.copy()

            context = params.context
            domain = params.domain

            if isinstance(domain, basestring):
                domain = eval(domain, ctx)

            if isinstance(context, basestring):
                if not context.startswith('{'):
                    context = "dict(%s)"%context
                    ctx.dict = dict # required

                context = eval(context, ctx)

            search_domain.extend(domain)

            params.domain = domain
            params.context = context

        if fields_type:
            for n, v in fields_type.items():
                t = _make_domain(n, v, data.get(n))
                if t:
                    search_domain += t

        try:
            l = int(data.get('limit', 20))
            o = int(data.get('offset', 0))
        except:
            l = 20
            o = 0

        if l < 1: l = 20
        if o < 0: o = 0
        proxy = rpc.RPCProxy(params.model)
        params.found_ids = proxy.search(search_domain, o, l)

        data['limit'] = l
        data['offset'] = o

        return self.create(params, data)
