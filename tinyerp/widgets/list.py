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

from elementtree import ElementTree as ET

from turbogears import widgets

from tinyerp import rpc
from tinyerp import tools

class List(widgets.Widget):
    params = ['data', 'headers', 'model', 'selectable', 'editable']
    template = "tinyerp.widgets.templates.list"

    css = [widgets.CSSLink(widgets.static, "grid.css"), widgets.CSSLink('tinyerp', 'css/ajaxlist.css')]

    def __init__(self, model, view, ids=[], domain=[], context={}, selectable=False, editable=False):

        self.selectable = selectable
        self.editable = editable

        self.ids = ids

        fields = view['fields']
        dom = xml.dom.minidom.parseString(view['arch'])
        root = dom.childNodes[0]

        attrs = tools.node_attributes(root)
        self.string = attrs.get('string','')

        data = []
        if ids == None or len(ids) > 0:
            proxy = rpc.RPCProxy(model)
            ids = ids or proxy.search([])
            data = proxy.read(ids, fields)

            self.ids = ids

        self.headers, self.data = self.parse(root, fields, data)

    def parse(self, root, fields, data=[]):
        """Parse the given node to generate valid list headers.

        @param root: the root node of the view
        @param fields: the fields

        @return: an instance of turbogears.widgets.DataGrid
        """

        headers = []

        for node in root.childNodes:

            if node.nodeName=='field':
                attrs = tools.node_attributes(node)

                if attrs.has_key('name'):
                    name = attrs.get('name')
                    type = fields[name]['type']

                    fields[name].update(attrs)

                    if type not in CELLTYPES: continue

                    for row in data:
                        cell = CELLTYPES[type](attrs=fields[name])
                        row[name] = cell.get_value(row[name])

                    headers += [(name, fields[name]['string'])]

        return headers, data

class Char(object):

    def __init__(self, attrs={}):
        self.attrs = attrs

    def get_value(self, value):
        return unicode(value or '', 'utf-8')

class M2O(Char):

    def get_value(self, value):
        if value and len(value) > 0:
            return str(value[-1])

        return ''

class Date(Char):

    server_format = '%Y-%m-%d'
    display_format = '%x'

    def get_value(self, value):
        if value:
            date = time.strptime(value, self.server_format)
            return time.strftime(self.display_format, date)

        return ''

class O2M(Char):

    def get_value(self, value):
        return "(%d)" % len(value)

class M2M(Char):

    def get_value(self, value):
        return "(%d)" % len(value)

class Selection(Char):

    def get_value(self, value):
        if value:
            selection = self.attrs['selection']
            for k, v in selection:
                if k == value:
                    return v
        return ''

class Float(Char):

    def get_value(self, value):
        _, digit = (16,2)

        if value:
            return locale.format('%.' + str(digit) + 'f', value or 0.0)

        return value

class Int(Char):

    def get_value(self, value):
        if value:
            return int(value)

        return value

class DateTime(Char):
    server_format = '%Y-%m-%d %H:%M:%S'
    display_format = '%x %H:%M:%S'

    def get_value(self, value):
        if value:
            date = time.strptime(value, self.server_format)
            return time.strftime(self.display_format, date)

        return ''

class Boolean(Char):

    def get_value(self, value):
        if int(value) == 1:
            return 'True'
        else:
            return 'Flase'

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

