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
import types
import base64

import csv
import StringIO

from turbogears import expose
from turbogears import controllers

import cherrypy

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp.tinyres import TinyResource
from tinyerp.modules.utils import TinyDict

import tinyerp.widgets as tw

def datas_read(ids, model, fields):
    return rpc.RPCProxy(model).export_data(ids, fields)

def export_csv(fields, result, write_title=False):    
    try:
        fp = StringIO.StringIO()
        writer = csv.writer(fp)
        if write_title:
            writer.writerow(fields)
        for data in result:
            row = []
            for d in data:
                if type(d)==types.StringType:
                    row.append(d.replace('\n',' ').replace('\t',' '))
                else:
                    row.append(d)
            writer.writerow(row)

        fp.seek(0)
        data = fp.read()        
        fp.close()
        
        return data
    except IOError, (errno, strerror):
        raise common.message(_("Operation failed !\nI/O error")+"(%s)" % (errno,))

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

        is_importing = len(eval(kw.get('domain')))
                    
        ids = kw.get('ids', '').split(',')               
        ids = [i for i in ids if i]

        proxy = rpc.RPCProxy(model)
        fields = proxy.fields_get(False, rpc.session.context)
        
        fields_order = fields.keys()        
        fields_order.sort(lambda x,y: -cmp(fields[x].get('string', ''), fields[y].get('string', '')))

        records = []

        for i, field in enumerate(fields_order):
            
            value = fields[field]
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
            record['data'] = {'name' : nm}
            
            records += [record]

            if len(nm.split('/')) < 3 and value.get('relation', False):
                                                
                if is_importing and not ((value['type'] not in ('reference',)) and (not value.get('readonly', False)) and value['type']=='one2many'):
                    continue
                
                ref = value.pop('relation')
            
                proxy = rpc.RPCProxy(ref)
                cfields = proxy.fields_get(False, rpc.session.context)                    
                cfields_order = cfields.keys()
                cfields_order.sort(lambda x,y: -cmp(cfields[x].get('string', ''), cfields[y].get('string', '')))
                                    
                children = []
                for j, fld in enumerate(cfields_order):
                    cid = id + '/' + fld
                    cid = cid.replace(' ', '_')
                    
                    children += [cid]

                record['children'] = children
                record['params'] = {'model': ref, 'prefix': id, 'name': nm}            
        
        records.reverse()            
        return dict(records=records)
    
    @expose(content_type="application/octat-stream")
    def export_data(self, fields, export_as="csv", add_names=False, **kw):
        params, data = TinyDict.split(kw)
        
        result = datas_read(params.ids, params.model, fields)
        
        if export_as == 'excel':
            #add_names = True
            pass

        return export_csv(params.fields2, result, add_names)
    
    @expose(template="tinyerp.modules.gui.templates.imp")
    def imp(self, **kw):
        params, data = TinyDict.split(kw)
        
        headers = [{'string' : 'Name', 'name' : 'name', 'type' : 'char'}]        
        tree = tw.treegrid.TreeGrid('import_fields', model=params.model, headers=headers, url='/impex/get_fields', field_parent='relation')
        tree.show_headers = False
        tree.domain = [()] # will be used in `get_fields` as flag

        return dict(model=params.model, source=params.source, tree=tree, show_header_footer=False)
    