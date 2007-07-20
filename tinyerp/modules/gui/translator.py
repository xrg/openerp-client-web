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

import os
import copy

from turbogears import expose
from turbogears import controllers

import cherrypy

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp.tinyres import TinyResource
from tinyerp.modules.utils import TinyDict

import tinyerp.widgets as tw

#change 'en' to false for context
def adapt_context(val):
    if val == 'en_US':
        return False
    else:
        return val

class Translator(controllers.Controller, TinyResource):

    @expose(template="tinyerp.modules.gui.templates.translator")
    def index(self, translate='fields', **kw):        
        params, data = TinyDict.split(kw)
            
        proxy = rpc.RPCProxy('res.lang')

        lang_ids = proxy.search([('translatable', '=', '1')])
        langs = proxy.read(lang_ids, ['code', 'name'])
        
        proxy = rpc.RPCProxy(params.model)

        data = []
        view = []
                
        #view_fields = proxy.fields_view_get(False, 'form', rpc.session.context)['fields']
        view_fields = proxy.fields_get(False, rpc.session.context)

        names = view_fields.keys()
        names.sort(lambda x,y: cmp(view_fields[x].get('string', ''), view_fields[y].get('string', '')))
        
        if translate == 'fields' and params.id:                        
            for name in names:
                attrs = view_fields[name]
                if attrs.get('translate'):
                    value = {}
                    for lang in langs:
                        context = copy.copy(rpc.session.context)
                        context['lang'] = adapt_context(lang['code'])

                        val = proxy.read([params.id], [name], context)
                        val = val[0]

                        value[lang['code']] = val[name]

                    data += [(name, value)]        
        
        if translate == 'labels':
            for name in names:
                attrs = view_fields[name]
                if attrs.get('string'):
                    value = {}
                    for lang in langs:
                        code=lang['code']
                        val = proxy.read_string(False, [code], [name])
                        
                        if name in val[code]:
                            value[code] = val[code][name]

                    if value: data += [(name, value)]                        
            
        if translate == 'view':
            for lang in langs:
                code=lang['code']
                view_item_ids = rpc.session.execute('object', 'execute', 'ir.translation', 'search', [('name', '=', params.model), ('type', '=', 'view'), ('lang', '=', code)])
                view_items = rpc.session.execute('object', 'execute', 'ir.translation', 'read', view_item_ids, ['src', 'value'])

                values = []
                for val in view_items:
                    values += [val]

                if values:
                    view += [(code, values)]
                                                    
        return dict(translate=translate, langs=langs, data=data, view=view, model=params.model, id=params.id, show_header_footer=False)
    
    @expose()
    def save(self, translate='fields', **kw):
        params, data = TinyDict.split(kw)
        
        if translate == 'fields':
            if not params.id:
                raise common.error(_("You need to save ressource before adding translations."))
            
            for lang, value in data.items():                                
                
                context = copy.copy(rpc.session.context)
                context['lang'] = adapt_context(lang)
                                
                for name, val in value.items():
                    if isinstance(val, basestring):
                        val = [val]
                    
                    for v in val:
                        rpc.session.execute('object', 'execute', params.model, 'write', [params.id], {name : v}, context)
                    
        if translate == 'labels':
            for lang, value in data.items():
                for name, val in value.items():
                    rpc.session.execute('object', 'execute', params.model, 'write_string', False, [lang], {name: val})

        if translate == 'view':
            for lang, value in data.items():
                for id, val in value.items():
                    rpc.session.execute('object', 'execute', 'ir.translation', 'write', [int(id)], {'value': val})

        return self.index(translate=translate, _terp_model=params.model, _terp_id=params.id)
      
          
