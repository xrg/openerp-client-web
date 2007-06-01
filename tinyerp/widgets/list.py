###############################################################################
#
# Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id: list.py 5 2007-03-23 06:13:51Z ame $
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

import locale
import time
import xml.dom.minidom

from turbogears import widgets

from tinyerp import rpc
from tinyerp import tools

from interface import TinyCompoundWidget

class ListOptions(object):
    
    def __init__(self):        
        
        self.on_next = None
        self.on_previous = None
        self.on_first = None
        self.on_last = None
        
        self.on_select = None
        self.do_select = None
        
        self.show_links = True
        
class List(TinyCompoundWidget):

    params = ['name', 'data', 'columns', 'headers', 'model', 'selectable', 'editable', 'pageable', 'selector', 'source', 'offset', 'limit', 'options']
    template = "tinyerp.widgets.templates.list"

    data = None
    columns = 0
    headers = None
    model = None
    selectable = False
    editable = False
    source = None
    
    options = None
        
    css = [widgets.CSSLink('tinyerp', 'css/listview.css')]
    javascript = [widgets.JSLink('tinyerp', 'javascript/listview.js')]

    def __init__(self, name, model, view, ids=[], domain=[], context={}, **kw):

        super(List, self).__init__()

        self.name = name
        self.model = model
        self.ids = ids

        if name.endswith('/'):
            self.name = name[:-1]

        if name != '_terp_list':
            self.source = self.name.replace('/', '.') or None
            
        self.selectable = kw.get('selectable', 0)
        self.editable = kw.get('editable', False)
        self.pageable = kw.get('pageable', True)
        
        self.offset = kw.get('offset', 0)
        self.limit = kw.get('limit', 0)
        
        self.selector = 'checkbox'

        if self.selectable == 1:
            self.selector = 'radio'

        fields = view['fields']
        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]

        attrs = tools.node_attributes(root)
        self.string = attrs.get('string','')
        
        proxy = rpc.RPCProxy(model)
        
        if ids == None:
            if self.limit > 0:
                ids = proxy.search(domain, self.offset, self.limit)
            else:
                ids = proxy.search(domain)

        data = []
        if len(ids) > 0:
               
            ctx = rpc.session.context.copy()
            ctx.update(context)

            data = proxy.read(ids, fields, ctx)

            self.ids = ids

        self.headers, self.data = self.parse(root, fields, data)
        
        self.columns = len(self.headers) 
        
        self.columns += (self.selectable or 0) and 1
        self.columns += (self.editable or 0) and 2  
        
        self.options = ListOptions()      

    def parse(self, root, fields, data=[]):
        """Parse the given node to generate valid list headers.

        @param root: the root node of the view
        @param fields: the fields

        @return: an instance of List
        """
                
        headers = []
                
        for node in root.childNodes:
            if node.nodeName=='field':
                attrs = tools.node_attributes(node)
                                
                if 'name' in attrs:
                    
                    name = attrs['name']
                    kind = fields[name]['type']
                    
                    if kind not in CELLTYPES: 
                        continue
                                        
                    fields[name].update(attrs)                                    

                    for row in data:
                        row[name] = CELLTYPES[kind](attrs=fields[name], value=row[name])

                    headers += [(name, fields[name])]

        return headers, data    
    

from tinyerp.stdvars import tg_query

class Char(object):

    def __init__(self, attrs={}, value=False):
        self.attrs = attrs        
        self.value = value

        self.text = self.get_text()
        self.link = self.get_link()
           
    def get_text(self):
        return self.value or ''
    
    def get_link(self):
        return None

    def __str__(self):
        return ustr(self.text)
                
class M2O(Char):

    def get_text(self):
        if self.value and len(self.value) > 0:
            return self.value[-1]
        
        return ''
    
    def get_link(self):
        return tg_query('/form/view', model=self.attrs['relation'], id=(self.value or False) and self.value[0])
    
class Date(Char):

    server_format = '%Y-%m-%d'
    display_format = '%x'

    def get_text(self):
        try:
            date = time.strptime(self.value, self.server_format)
            return time.strftime(self.display_format, date)
        except:
            return ''

class O2M(Char):

    def get_text(self):
        return "(%d)" % len(self.value)

class M2M(Char):

    def get_text(self):
        return "(%d)" % len(self.value)

class Selection(Char):

    def get_text(self):
        if self.value:
            selection = self.attrs['selection']
            for k, v in selection:
                if k == self.value:
                    return v
        return ''

class Float(Char):

    def get_text(self):
        _, digit = (16,2)

        if self.value:
            return locale.format('%.' + str(digit) + 'f', self.value or 0.0)

        return self.value

class Int(Char):

    def get_text(self):
        if self.value:
            return int(self.value)

        return self.value

class DateTime(Char):
    server_format = '%Y-%m-%d %H:%M:%S'
    display_format = '%x %H:%M:%S'

    def get_text(self):
        try:
            date = time.strptime(self.value, self.server_format)
            return time.strftime(self.display_format, date)
        except:
            return ''

class Boolean(Char):

    def get_text(self):
        if int(self.value) == 1:
            return 'True'
        else:
            return 'False'

CELLTYPES = {
        'char':Char,
        'many2one':M2O,
        'date':Date,
        'one2many':O2M,
        'many2many':M2M,
        'selection':Selection,
        'float':Float,
        'integer':Int,
        'datetime':DateTime,
        'boolean' : Boolean
}

