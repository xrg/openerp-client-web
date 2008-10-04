###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

"""
This module implementes search view for a tiny model. Currently it simply displays
list view of the given model.
"""
import cherrypy

from turbogears import expose
from turbogears import widgets
from turbogears import redirect
from turbogears import controllers

from openerp import rpc
from openerp import tools
from openerp import common

from openerp import widgets as tw
from openerp import widgets_search as tws

from openerp.tinyres import TinyResource

from openerp.utils import TinyDict
from openerp.utils import TinyForm

def make_domain(name, value):

    if isinstance(value, int) and not isinstance(value, bool):
        return [(name, '=', value)]

    if isinstance(value, dict):

        start = value.get('from')
        end = value.get('to')

        if start and end:
            return [(name, '>=', start), (name, '<=', end)]

        elif start:
            return [(name, '>=', start)]

        elif end:
            return [(name, '<=', end)]

        return None

    if isinstance(value, basestring) and value:
        return [(name, 'ilike', value)]

    if isinstance(value, bool) and value:
        return [(name, '=', 1)]

    return []

from turbogears import validate, validators

def search(model, offset=0, limit=20, domain=[], context={}, data={}):

    domain = domain or []
    context = context or {}
    data = data or {}

    search_domain = domain[:]
    search_data = {}

    for k, v in data.items():
        t = make_domain(k, v)

        if t:
            search_domain += t
            search_data[k] = v

    l = limit
    o = offset

    if l < 1: l = 20
    if o < 0: o = 0

    proxy = rpc.RPCProxy(model)
    ctx = rpc.session.context.copy()
    ctx.update(context)

    ids = proxy.search(search_domain, o, l, 0, ctx)
    count = proxy.search_count(search_domain, ctx)

    return dict(model=model, ids=ids, count=count, search_domain=search_domain, search_data=search_data, offset=o, limit=l)

class Search(controllers.Controller, TinyResource):

    @expose(template="openerp.subcontrollers.templates.search")
    def create(self, params):

        params.view_mode = ['tree', 'form']

        params.offset = params.offset or 0
        params.limit = params.limit or 20
        params.count = params.count or 0

        search = tws.search.Search(model=params.model, domain=params.domain, context=params.context, values=params.search_data or {})
        screen = tw.screen.Screen(params=params, selectable=params.kind or 2)

        # don't show links in list view, except the do_select link
        screen.widget.show_links = 0

        return dict(search=search, screen=screen, params=params, show_header_footer=False)

    @expose()
    def new(self, model, source=None, kind=0, text=None, domain=[], context={}):
        """Create new search view...

        @param model: the model
        @param source: the source, in case of m2m, m2o search
        @param kind: 0=normal, 1=m2o, 2=m2m
        @param text: do `name_search` if text is provided
        @param domain: the domain
        @param context: the context
        """

        params = TinyDict()

        params.model = model
        params.domain = domain
        params.context = context

        params.source = source
        params.kind = kind

        if text:
            params.ids = []
            proxy = rpc.RPCProxy(model)
            ids = proxy.name_search(text, params.domain or [], 'ilike', params.context or {})
            if ids:
                params.ids = [id[0] for id in ids]
                params.count = len(ids)

        return self.create(params)

    @expose('json')
    def eval_domain_and_context(self, **kw):
        params, data = TinyDict.split(kw)
        
        domain = params.domain
        context = params.context
        parent_context = params.parent_context or {}
        
        parent_context.update(rpc.session.context.copy())

        ctx = TinyForm(**kw).to_python()
        pctx = ctx

        prefix = params.prefix
        if prefix:
            ctx = ctx.chain_get(prefix)

        if prefix and '/' in prefix:
            prefix = prefix.rsplit('/', 1)[0]
            pctx = pctx.chain_get(prefix)

        ctx['parent'] = pctx
        ctx['context'] = parent_context

        if isinstance(domain, basestring):
            domain = eval(domain, ctx)  
        
        if isinstance(context, basestring):
            if not context.startswith('{'):
                context = "dict(%s)"%context
                ctx['dict'] = dict # required
            
            ctx['active_id'] = params.parent_id or False
            context = eval(context, ctx)

#           Fixed many2one pop up in listgrid when value is None.
            for key, val in context.items():
                if val==None:
                    context[key] = False

        return dict(domain=ustr(domain), context=ustr(context))

    @expose()
    def filter(self, **kw):
        params, data = TinyDict.split(kw)
        
        l = params.limit or 20
        o = params.offset or 0

        domain = params.domain

        if params.search_domain is not None:
            domain = params.search_domain
            data = params.search_data

        res = search(params.model, o, l, domain=params.domain, data=data)

        params.ids = res['ids']
        params.offset = res['offset']
        params.limit = res['limit']
        params.count = res['count']
        params.search_domain = res['search_domain']
        params.search_data = res['search_data']

        return self.create(params)

    @expose()
    def find(self, **kw):

        kw['_terp_offset'] = None
        kw['_terp_limit'] = None

        kw['_terp_search_domain'] = None
        kw['_terp_search_data'] = None

        return self.filter(**kw)

    @expose()
    def first(self, **kw):
        params, data = TinyDict.split(kw)

        l = params.limit or 20
        o = 0

        kw['_terp_offset'] = o

        return self.filter(**kw)

    @expose()
    def previous(self, **kw):
        params, data = TinyDict.split(kw)

        l = params.limit or 20
        o = params.offset or 0

        o -= l

        kw['_terp_offset'] = o

        return self.filter(**kw)

    @expose()
    def next(self, **kw):
        params, data = TinyDict.split(kw)

        l = params.limit or 20
        o = params.offset or 0

        o += l

        kw['_terp_offset'] = o

        return self.filter(**kw)

    @expose()
    def last(self, **kw):
        params, data = TinyDict.split(kw)

        l = params.limit or 20
        o = params.offset or 0
        c = params.count or 0

        o = c - (c % l)

        kw['_terp_offset'] = o

        return self.filter(**kw)

    @expose('json')
    def ok(self, **kw):
        params, data = TinyDict.split(kw)

        ids = [int(id) for id in data.get('search_list', [])]
        return dict(ids=ids)

    @expose('json')
    def get_name(self, model, id):
        name = tw.many2one.get_name(model, id)
        if not name:
            name=''
        return dict(name=name)

    @expose('json')
    def get_matched(self, model, text, **kw):
        params, data = TinyDict.split(kw)

        domain = params.domain or []
        context = params.context or {}
        
        ctx = rpc.session.context.copy()
        ctx.update(context)

        proxy = rpc.RPCProxy(model)
        values = proxy.name_search(text, domain, 'ilike', ctx)
        
        return dict(values=values)

    @expose()
    def get_m2m(self, model, ids, list_id):
        if not ids:
            ids='[]'
        ids = eval(ids)

        if not isinstance(ids, (list, tuple)): ids = [ids]

        m2m = tw.many2many.M2M(dict(relation=model, value=ids, name=list_id))
        return m2m.screen.render()
    
# vim: ts=4 sts=4 sw=4 si et

