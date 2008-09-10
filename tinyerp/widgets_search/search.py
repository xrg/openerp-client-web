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
# along with this program; if not, write to the 
# Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
# Boston, MA  02111-1307, USA.
#
###############################################################################

"""
This module implementes widget parser for form view, and
several widget components.
"""
import xml.dom.minidom

import cherrypy
import turbogears as tg

from tinyerp import rpc
from tinyerp import tools
from tinyerp import cache

from tinyerp.widgets.interface import TinyInputWidget
from tinyerp.widgets.interface import TinyCompoundWidget

from tinyerp.widgets.form import Char
from tinyerp.widgets.form import Form
from tinyerp.widgets.form import Frame
from tinyerp.widgets.form import Button
from tinyerp.widgets.form import Float
from tinyerp.widgets.form import Frame
from tinyerp.widgets.form import DateTime
from tinyerp.widgets.form import Integer
from tinyerp.widgets.form import Selection
from tinyerp.widgets.form import Notebook

class RangeWidget(TinyCompoundWidget):
    template = "tinyerp.widgets_search.templates.rangewid"

    params = ["field_value"]
    member_widgets = ["from_field", "to_field"]

    def __init__(self, attrs):
        super(RangeWidget, self).__init__(attrs)

        kind = attrs.get('type', 'integer')

        fname = attrs['name']

        from_attrs = attrs.copy()
        to_attrs = attrs.copy()

        from_attrs['name'] = fname + '/from'
        to_attrs['name'] = fname + '/to'

        self.from_field = range_widgets_type[kind](from_attrs)
        self.to_field = range_widgets_type[kind](to_attrs)

        # in search view fields should be writable
        self.from_field.readonly = False
        self.to_field.readonly = False

    def set_value(self, value):
        start = value.get('from', '')
        end = value.get('to', '')

        self.from_field.set_value(start)
        self.to_field.set_value(end)

class Search(TinyCompoundWidget):
    template = "tinyerp.widgets_search.templates.search"
    params = ['fields_type']
    member_widgets = ['_notebook', 'basic', 'advance']

    _notebook = Notebook({}, [])

    def __init__(self, model, domain=[], context={}, values={}):

        super(Search, self).__init__({})

        self.model         = model

        self.domain        = domain
        self.context       = context

        ctx = rpc.session.context.copy()
        self.view = cache.fields_view_get(self.model, False, 'form', ctx, True)

        fields = self.view['fields']

        dom = xml.dom.minidom.parseString(self.view['arch'].encode('utf-8'))
        root = dom.childNodes[0]
        attrs = tools.node_attributes(root)
        self.string = attrs.get('string', '')

        self.fields_type = {}
        self.widgets = []
        self.parse(dom, fields, values)

        self.basic = Frame({}, [w for w in self.widgets if not w.adv])
        self.advance = Frame({}, self.widgets)

    def parse(self, root=None, fields=None, values={}):

        for node in root.childNodes:

            if not node.nodeType==node.ELEMENT_NODE:
                continue

            attrs = tools.node_attributes(node)

            if attrs.has_key('colspan'):
                attrs['colspan'] = 1

            if attrs.has_key('nolabel'):
                attrs['nolabel'] = False

            if node.localName == 'form':
                self.parse(root=node, fields=fields, values=values)
                #views += [Frame(attrs, n)]

            elif node.localName == 'notebook':
                self.parse(root=node, fields=fields, values=values)

            elif node.localName == 'page':
                self.parse(root=node, fields=fields, values=values)

            elif node.localName=='group':
                self.parse(root=node, fields=fields, values=values)

            elif node.localName == 'field':
                name = attrs['name']

                if not ('select' in attrs or 'select' in fields[name]):
                    continue

                if attrs.get('widget', False):
                    if attrs['widget']=='one2many_list':
                        attrs['widget']='one2many'
                    attrs['type'] = attrs['widget']

                # in search view fields should be writable
                attrs['readonly'] = False
                attrs['required'] = False
                attrs['translate'] = False
                attrs['disabled'] = False
                attrs['visible'] = True
                attrs['editable'] = True

                try:
                    fields[name].update(attrs)
                except:
                    print "-"*30,"\n malformed tag for :", attrs
                    print "-"*30
                    raise
                
                kind = fields[name]['type']

                if kind not in widgets_type:
                    continue

                self.fields_type[name] = kind

                field = widgets_type[kind](attrs=fields[name])
                field.onchange = None
                field.callback = None

                val = fields[name].get('select', False)
                field.adv = val and int(val) > 1

                if kind == 'boolean':
                    field.options = [[1,'Yes'],[0,'No']]
                    field.validator.if_empty = ''

                if values.has_key(name) and isinstance(field, (TinyInputWidget, RangeWidget)):
                    field.set_value(values[name])

                self.widgets += [field]

range_widgets_type = {
    'date': DateTime,
    'time': DateTime,
    'datetime': DateTime,
    'float': Float,
    'integer': Integer,
}

widgets_type = {
    'date': RangeWidget,
    'datetime': RangeWidget,
    'float': RangeWidget,
    'integer': RangeWidget,
    'selection': Selection,
    'char': Char,
    'boolean': Selection,
    #'reference': Reference,
    #'binary': Binary,
    #'picture': Picture,
    'text': Char,
    #'text_tag': TextTag,
    'one2many': Char,
    'one2many_form': Char,
    'one2many_list': Char,
    'many2many': Char,
    'many2one': Char,
    'email' : Char,
    'url' : Char,
    #'image' : Image,
}

# vim: ts=4 sts=4 sw=4 si et

