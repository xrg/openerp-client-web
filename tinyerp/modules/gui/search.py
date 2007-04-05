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

@todo: implement read search window
"""
import cherrypy

from turbogears import expose
from turbogears import widgets
from turbogears import controllers

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp import tools
from tinyerp import widgets as tw
from tinyerp import widgets_search as tws
from tinyerp.tinyres import TinyResource

import form

from utils import MyDict
from utils import make_dict
from utils import terp_split

def _search_string(name, type, value):
    if value:

        if type == 'many2many' or type == 'one2many' or type =='many2one' or type=='char':
            return name, 'ilike', value

        elif type== 'float' or type == 'integer' or type == 'datetime' or type=='date' or type=='time':
            if value[0] and value[1]:
                return [(name, '>=', value[0]), (name, '<=', value[1])]
            elif value[0]:
                return name, '>=', value[0]
            elif value[1]:
                return name, '<=', value[1]
            return None

        elif type=='boolean' or type=='selection':
            return name, '=', int(value)

    return None

class Search(controllers.Controller, TinyResource):

    @expose(template="tinyerp.modules.gui.templates.search")
    def create(self, model, textid=None, hiddenname=None, s_domain=[], id=None, ids=[], state='', view_ids=[], view_mode=['form', 'tree'], view_mode2=['tree', 'form'], domain=[], context={}):
        """Create search view...

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

        proxy = rpc.RPCProxy(model)

        view_form = proxy.fields_view_get({}, 'form', {})
        view_tree = proxy.fields_view_get({}, 'tree', {})

        form_view = tws.search_form.Form(prefix='', model=model, ids=ids, view=view_form, domain=domain, context=context)
        list_view = tw.list.List(model=model, ids=ids or [], view=view_tree, domain=domain, context=context, selectable=True)

        return dict(form_view=form_view, list_view=list_view, model=model, id=id, ids=ids, state=state, view_ids=view_ids, view_mode=view_mode, view_mode2=view_mode2, domain=domain, context=context, textid=textid, hiddenname=hiddenname, s_domain=s_domain)

    @expose()
    def ok(self, **kw):
        terp, data = terp_split(kw)

        ids = data.get('check', None)

        if ids:
            if type(ids) == type([]):
                terp.ids = [int(e) for e in ids]
            else:
                terp.ids = [int(ids)]
            terp.id = terp.ids[0]

        terp.pop('fields_type')
        return form.Form().create(**terp)

    @expose()
    def cancel(self, **kw):
        terp, data = terp_split(kw)
        terp.ids = cherrypy.session.get('_terp_ids', [])

        terp.pop('fields_type')
        return form.Form().create(**terp)

    @expose()
    def find(self, **kw):

        s_domain = kw.get('s_domain',[])
        s_domain = eval(s_domain)

        terp, data = terp_split(kw)
        fields_type = eval(terp.pop('fields_type'))
        search_list = s_domain
        if fields_type:
            for n, v in fields_type.items():
                t = _search_string(n, v, kw[n])
                if t:
                    if type(t) == type([]):
                        search_list += t
                    else:
                        search_list += [t]

        try:
            l = int(data.get('limit', '80'))
            o = int(data.get('offset', '0'))
        except:
            l = 80
            o = 0

        if data.has_key('textid'):
            terp['textid'] = data.pop('textid')
        if data.has_key('hiddenname'):
            terp['hiddenname'] = data.pop('hiddenname')
        if data.has_key('s_domain'):
            terp['s_domain'] = data.pop('s_domain')
        proxy = rpc.RPCProxy(terp.model)
        terp.ids = proxy.search(search_list, o, l)
        return self.create(**terp)

    @expose('json')
    def get_string(self,model,id):
        proxy = rpc.RPCProxy(model)
        name = proxy.name_get([id], {})
        return dict(name=name[0][1])

