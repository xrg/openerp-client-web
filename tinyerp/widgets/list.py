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
       
class Pager(TinyCompoundWidget):

    template = "tinyerp.widgets.templates.pager"
    params = ['offset', 'limit', 'count', 'total', 'prev', 'next', 'page_info']

    css = [widgets.CSSLink('tinyerp', 'css/pager.css')]

    offset = 0
    limit = 20
    count = 0
    
    page_info = None

    def __init__(self, id=False, ids=[], offset=0, limit=20, count=0, view_mode=['tree','form']):
        
        super(Pager, self).__init__()

        self.limit = limit or 20
        self.offset = offset or 0
        self.count = count
        
        self.id = id or False
        self.ids = ids or []
        
        if view_mode[0] == 'form':
            index = 0            
            if self.id in self.ids:
                index = self.offset + self.ids.index(self.id) + 1

            self.page_info = "[%s/%s]" % (index or '-', self.count)
                        
            self.prev = index > 1
            self.next = index < self.count

        else:
            self.page_info = "[%s - %s of %s]" % (self.offset+1, self.offset + len(self.ids), self.count)
            self.prev = self.offset > 0
            self.next = self.offset+len(self.ids) < self.count
                        
class List(TinyCompoundWidget):

    template = "tinyerp.widgets.templates.list"
    params = ['name', 'data', 'columns', 'headers', 'model', 'selectable', 'editable', 'pageable', 'selector', 'source', 'offset', 'limit', 'show_links']
    member_widgets = ['pager']

    pager = None

    data = None
    columns = 0
    headers = None
    model = None
    selectable = False
    editable = False
    pageable = False
    show_links = 1
    source = None

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
        self.count = kw.get('count', 0)

        self.selector = None

        if self.selectable == 1:
            self.selector = 'radio'

        if self.selectable == 2:
            self.selector = 'checkbox'

        fields = view['fields']
        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]

        attrs = tools.node_attributes(root)
        self.string = attrs.get('string','')

        self.colors = {}
        for color_spec in attrs.get('colors', '').split(';'):
            if color_spec:
                colour, test = color_spec.split(':')
                self.colors[colour] = test

        proxy = rpc.RPCProxy(model)

        if ids == None:            
            if self.limit > 0:
                ids = proxy.search(domain, self.offset, self.limit)
            else:
                ids = proxy.search(domain)
                
            self.count = proxy.search_count(domain)

        data = []
        if len(ids) > 0:

            ctx = rpc.session.context.copy()
            ctx.update(context)

            data = proxy.read(ids, fields.keys(), ctx)

            self.ids = ids

        self.headers, self.data = self.parse(root, fields, data)

        self.columns = len(self.headers)

        self.columns += (self.selectable or 0) and 1
        self.columns += (self.editable or 0) and 2

        if self.pageable:            
            self.pager = Pager(ids=self.ids, offset=self.offset, limit=self.limit, count=self.count)

    def parse(self, root, fields, data=[]):
        """Parse the given node to generate valid list headers.

        @param root: the root node of the view
        @param fields: the fields

        @return: an instance of List
        """

        headers = []
        values  = [row.copy() for row in data]

        for node in root.childNodes:
            if node.nodeName=='field':
                attrs = tools.node_attributes(node)

                if 'name' in attrs:

                    name = attrs['name']
                    kind = fields[name]['type']

                    if kind not in CELLTYPES:
                        continue

                    fields[name].update(attrs)

                    invisible = fields[name].get('invisible', False)
                    if isinstance(invisible, basestring):
                        invisible = eval(invisible)

                    if invisible:
                        continue

                    for i, row in enumerate(data):

                        row_value = values[i]

                        cell = CELLTYPES[kind](attrs=fields[name], value=row_value[name])

                        for color, expr in self.colors.items():
                            try:
                                if tools.expr_eval(expr, row_value):
                                    cell.color = color
                                    break
                            except:
                                pass

                        row[name] = cell

                    headers += [(name, fields[name])]

        # generate do_select links
        if self.selectable:
            name, field = headers[0]
            for row in data:
                cell = row[name]

                if self.selectable:
                    cell.link = "javascript: void(0)"
                    cell.onclick = "do_select(%s, '%s'); return false;"%(row['id'], self.name)

        return headers, data

from tinyerp.stdvars import tg_query

class Char(object):

    def __init__(self, attrs={}, value=False):
        self.attrs = attrs
        self.value = value

        self.text = self.get_text()
        self.link = self.get_link()

        self.color = None
        self.onclick = None

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

        return self.value or ''

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
            return 'Yes'
        else:
            return 'No'

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

