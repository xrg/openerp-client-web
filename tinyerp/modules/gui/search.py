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
from turbogears import redirect
from turbogears import controllers

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp import tools
from tinyerp import widgets as tw
from tinyerp import widgets_search as tws

from tinyerp.tinyres import TinyResource

from tinyerp.modules.utils import TinyDict
from tinyerp.modules.utils import TinyParent

def make_domain(name, value):
    
    if not value:
        return []
    
    elif isinstance(value, dict):
                    
        start = value.get('from')
        end = value.get('to')            
        
        if start and end:
            return [(name, '>=', start), (name, '<=', end)]
        elif start:
            return [(name, '>=', start)]
        elif end:
            return [(name, '<=', end)]
        return None
    
    elif isinstance(value, (int, bool)):
        return [(name, '=', int(value))]
    
    else:
        return [(name, 'ilike', value)]

from turbogears import validate, validators

def search(model, offset=0, limit=20, domain=[], data={}):
    
    domain = domain or []
    data = data or {}

    search_domain = []
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
                            
    ids = proxy.search(search_domain, o, l)
            
    return dict(model=model, ids=ids, search_domain=search_domain, search_data=search_data, offset=o, limit=l)
  
class Search(controllers.Controller, TinyResource):

    @expose(template="tinyerp.modules.gui.templates.search")
    def create(self, params):
        
        params.view_mode = ['tree', 'form']
        
        params.setdefault('limit', 20)
        params.setdefault('offset', 0)
                        
        search = tws.search.Search(model=params.model, domain=params.domain, context=params.context, values=params.search_data or {})        
        screen = tw.screen.Screen(params=params, selectable=2)
        
        # don't show links in list view, except the do_select link
        screen.widget.show_links = 0
                
        return dict(search=search, screen=screen, params=params)
    
    @expose()
    def new(self, model, source=None, kind=0, domain=[], context={}):
        """Create new search view...
        
        @param model: the model
        @param source: the source, in case of m2m, m2o search
        @param kind: 0=normal, 1=m2o, 2=m2m
        @param domain: the domain
        @param context: the context
        """

        params = TinyDict()

        params.model = model
        params.domain = domain
        params.context = context
        
        params.source = source
        params.kind = kind
        
        return self.create(params)
    
    @expose('json')
    def eval_domain_and_context(self, **kw):
        params, data = TinyDict.split(kw)
                
        domain = params.domain
        context = params.context

        ctx = TinyParent(**kw)
        pctx = ctx

        prefix = params.prefix
        if prefix:
            ctx = ctx[prefix.replace('/', '.')]
            
        if prefix and '/' in prefix:
            prefix = prefix.rsplit('/', 1)[0]
            pctx = pctx[prefix.replace('/', '.')]

        ctx.parent = pctx
        ctx.context = rpc.session.context.copy()        

        if isinstance(domain, basestring):
            domain = eval(domain, ctx)

        if isinstance(context, basestring):
            if not context.startswith('{'):
                context = "dict(%s)"%context
                ctx.dict = dict # required

            context = eval(context, ctx)

        return dict(domain=ustr(domain), context=ustr(context))
            
    @expose()
    def filter(self, **kw):
        params, data = TinyDict.split(kw)
        
        l = params.get('limit') or 20
        o = params.get('offset') or 0

        res = search(params.model, o, l, domain=params.domain, data=data)
        params.update(res)
                        
        return self.create(params)

    @expose()
    def first(self, **kw):
        params, data = TinyDict.split(kw)
        
        l = params.get('limit') or 20
        o = 0

        kw['_terp_offset'] = o
        
        return self.filter(**kw)
    
    @expose()
    def previous(self, **kw):
        params, data = TinyDict.split(kw)
        
        l = params.get('limit') or 20
        o = params.get('offset') or 0
        
        o -= l
        
        kw['_terp_offset'] = o
        
        return self.filter(**kw)    
    
    @expose()
    def next(self, **kw):
        params, data = TinyDict.split(kw)
        
        l = params.get('limit') or 20
        o = params.get('offset') or 0            
        
        o += l
        
        kw['_terp_offset'] = o
                
        return self.filter(**kw)
        
    @expose()
    def last(self, **kw):
        #TODO: not implemented yet
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
    
    @expose()
    def get_list(self, model, ids, list_id):
        if not ids:
            ids='[]'
        ids = eval(ids)

        if not isinstance(ids, list): ids = [ids]

        m2m = tw.many2many.M2M(dict(relation=model, value=ids, name=list_id))
        return m2m.list_view.render()
    