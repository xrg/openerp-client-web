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
import time
import base64

from turbogears import expose
from turbogears import controllers

import cherrypy

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp.tinyres import TinyResource
from tinyerp.modules.utils import TinyDict

import tinyerp.widgets as tw

class ImpEx(controllers.Controller, TinyResource):
    
    @expose(template="tinyerp.modules.gui.templates.exp")
    def exp(self, **kw):
        params, data = TinyDict.split(kw)
        
        headers = [{'string' : 'Name', 'name' : 'name', 'type' : 'char'}]        
        tree = tw.treegrid.TreeGrid('export_fields', model=params.model, headers=headers, url='/impex/get_fields', field_parent='relation')
        tree.show_headers = False

        return dict(model=params.model, source=params.source, tree=tree, show_header_footer=False)
    
    @expose('json')
    def get_fields(self, model, prefix='', name='', field_parent=None, **kw):
               
        ids = kw.get('ids', '').split(',')               
        ids = [i for i in ids if i]

        proxy = rpc.RPCProxy(model)
        fields = proxy.fields_get(False, rpc.session.context)

        records = []

        for i, (field, value) in enumerate(fields.items()):
            record = {}
            
            id = prefix + (prefix and '/' or '') + field
            nm = name + (name and '/' or '') + value['string']
            
            if ids:
                record['id'] = ids[i]
            else:
                record['id'] = id

            record['action'] = 'javascript: void(0)'
            record['target'] = None
            
            record['icon'] = None
            
            record['children'] = []

            if len(nm.split('/')) < 3 and field_parent and field_parent in value:

                ref = value.pop(field_parent) or None
                if ref:
                    proxy = rpc.RPCProxy(ref)
                    fields = proxy.fields_get(False, rpc.session.context)

                    children = []
                    for j, fld in enumerate(fields):
                        cid = id + '/' + fld
                        cid = cid.replace(' ', '_')
                        
                        children += [cid]

                    record['children'] = children
                    record['params'] = {'model': ref, 'prefix': id, 'name': nm}

            record['data'] = {'name' : nm}

            records += [record]
        
        return dict(records=records)

    @expose(template="tinyerp.modules.gui.templates.imp")
    def imp(self, **kw):
        params, data = TinyDict.split(kw)
        return dict(model=params.model, source=params.source, show_header_footer=False)