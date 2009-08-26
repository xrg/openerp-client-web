###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# The OpenERP web client is distributed under the "OpenERP Public License".
# It's based on Mozilla Public License Version (MPL) 1.1 with following
# restrictions:
#
# -   All names, links and logos of Tiny, Open ERP and Axelor must be
#     kept as in original distribution without any changes in all software
#     screens, especially in start-up page and the software header, even if
#     the application source code has been changed or updated or code has been
#     added.
#
# -   All distributions of the software must keep source code with OEPL.
#
# -   All integrations to any other software must keep source code with OEPL.
#
# If you need commercial licence to remove this kind of restriction please
# contact us.
#
# You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################

"""
This module implementes widget parser for form view, and
several widget components.
"""
import xml.dom.minidom

import cherrypy

from openerp import rpc
from openerp import tools
from openerp import cache

from openerp.widgets.interface import TinyInputWidget

from openerp.widgets.form import Char
from openerp.widgets.form import Form
from openerp.widgets.form import Frame
from openerp.widgets.form import Button
from openerp.widgets.form import Float
from openerp.widgets.form import Frame
from openerp.widgets.form import DateTime
from openerp.widgets.form import Integer
from openerp.widgets.form import Selection
from openerp.widgets.form import Notebook

class RangeWidget(TinyInputWidget):
    template = "templates/rangewid.mako"

    params = ["field_value"]
    member_widgets = ["from_field", "to_field"]

    def __init__(self, **attrs):
        super(RangeWidget, self).__init__(**attrs)

        kind = attrs.get('type', 'integer')

        fname = attrs['name']

        from_attrs = attrs.copy()
        to_attrs = attrs.copy()

        from_attrs['name'] = fname + '/from'
        to_attrs['name'] = fname + '/to'

        self.from_field = RANGE_WIDGETS[kind](**from_attrs)
        self.to_field = RANGE_WIDGETS[kind](**to_attrs)

        #self.from_field.validator.if_invalid = False
        #self.to_field.validator.if_invalid = False

        # in search view fields should be writable
        self.from_field.readonly = False
        self.to_field.readonly = False
        
        # register the validators
        if hasattr(cherrypy.request, 'terp_validators'):
            for widget in [self.from_field, self.to_field]:
                cherrypy.request.terp_validators[str(widget.name)] = widget.validator
                cherrypy.request.terp_fields += [widget]

    def set_value(self, value):
        start = value.get('from', '')
        end = value.get('to', '')

        self.from_field.set_value(start)
        self.to_field.set_value(end)

class Search(TinyInputWidget):
    template = "templates/search.mako"
    params = ['fields_type']
    member_widgets = ['_notebook', 'basic', 'advance']

    _notebook = Notebook(name="search_notebook")

    def __init__(self, model, domain=[], context={}, values={}):

        super(Search, self).__init__(model=model)

        self.domain = domain or []
        self.context = context or {}

        ctx = rpc.session.context.copy()
        view = cache.fields_view_get(self.model, False, 'form', ctx, True)

        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]
        attrs = tools.node_attributes(root)
        self.string = attrs.get('string', '')

        self.fields_type = {}
        self.widgets = []
        self.parse(dom, view['fields'], values)

        # also parse the tree view
        view = cache.fields_view_get(self.model, False, 'tree', ctx, True)
        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        self.parse(dom, view['fields'], values)

        self.basic = Frame(children=[w for w in self.widgets if not w.adv])
        self.advance = Frame(children=self.widgets)

    def parse(self, root=None, fields=None, values={}):

        for node in root.childNodes:

            if not node.nodeType==node.ELEMENT_NODE:
                continue

            attrs = tools.node_attributes(node)

            if attrs.has_key('colspan'):
                attrs['colspan'] = 1

            if attrs.has_key('nolabel'):
                attrs['nolabel'] = False

            if node.localName in ('form', 'tree'):
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

                if name in self.fields_type:
                    continue

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
                attrs['invisible'] = False
                attrs['editable'] = True
                attrs['attrs'] = None

                try:
                    fields[name].update(attrs)
                except:
                    print "-"*30,"\n malformed tag for:", attrs
                    print "-"*30
                    raise

                kind = fields[name]['type']

                if kind not in WIDGETS:
                    continue

                self.fields_type[name] = kind

                field = WIDGETS[kind](**fields[name])
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

RANGE_WIDGETS = {
    'date': DateTime,
    'time': DateTime,
    'datetime': DateTime,
    'float': Float,
    'integer': Integer,
}

WIDGETS = {
    'date': RangeWidget,
    'datetime': RangeWidget,
    'float': RangeWidget,
    'integer': RangeWidget,
    'selection': Selection,
    'char': Char,
    'boolean': Selection,
    'text': Char,
    'one2many': Char,
    'one2many_form': Char,
    'one2many_list': Char,
    'many2many': Char,
    'many2one': Char,
    'email' : Char,
    'url' : Char,
}

# vim: ts=4 sts=4 sw=4 si et

