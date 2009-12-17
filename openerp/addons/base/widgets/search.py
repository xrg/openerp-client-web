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
import copy

import cherrypy
import random

from openerp import tools
from openerp.tools import rpc
from openerp.tools import cache
from openerp.tools import icons

from base.widgets import TinyInputWidget

from base.widgets.form import Char
from base.widgets.form import Form
from base.widgets.form import Frame
from base.widgets.form import Button
from base.widgets.form import Float
from base.widgets.form import Frame
from base.widgets.form import DateTime
from base.widgets.form import Integer
from base.widgets.form import Selection
from base.widgets.form import Notebook
from base.widgets.form import Separator
from base.widgets.form import Group
from base.widgets.form import NewLine

from base.widgets import JSLink, locations

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

class Filter(TinyInputWidget):
    template = "templates/filter.mako"
    
    params = ['icon', 'filter_domain', 'help', 'filter_id', 'text_val']
    
    def __init__(self, **attrs):
        super(Filter, self).__init__(**attrs)
        
        self.icon = attrs.get('icon')
        self.filter_domain = attrs.get('domain')
        self.help = attrs.get('help')
        self.filter_id = 'filter_%s' % (random.randint(0,10000))
        
        self.nolabel = True
        self.readonly = False
        
        self.text_val = self.string or self.help
        
        if self.icon:
            self.icon = icons.get_icon(self.icon)

class Search(TinyInputWidget):
    template = "templates/search.mako"
    javascript = [JSLink("base", "javascript/search.js", location=locations.bodytop)]
    
    params = ['fields_type', 'filters_list', 'middle_string', 'fields_list']
    member_widgets = ['frame']

    _notebook = Notebook(name="search_notebook")

    def __init__(self, model, domain=[], context={}, values={}):
        
        super(Search, self).__init__(model=model)

        self.domain = domain or []
        self.context = context or {}
        self.model = model

        ctx = rpc.session.context.copy()
        ctx.update(self.context)
        
        view_id = ctx.get('search_view') or False
        
        view = cache.fields_view_get(self.model, view_id, 'search', ctx, True)
        fields = cache.fields_get(self.model, [], ctx)
        
        self.fields_list = []
        
        for k,v in fields.items():
            if v['type'] in ('many2one', 'char', 'float', 'integer', 'date', 'datetime', 'selection', 'many2many', 'boolean', 'one2many') and v.get('selectable',  False):
                self.fields_list.append([k, v['string'], v['type']])
        if self.fields_list:
            self.fields_list.sort(lambda x, y: cmp(x[1], y[1]))
            
        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]
        attrs = tools.node_attributes(root)
        self.string = attrs.get('string', '')

        self.fields_type = {}
        
        self.frame = self.parse(model, dom, view['fields'], values)[0]
        
        my_acts = rpc.session.execute('object', 'execute', 'ir.actions.act_window', 'get_filters', model)
                
        sorted_filters = [[act.get('domain', act['id']), act['name']] for act in my_acts]
        sorted_filters.sort(lambda x, y: cmp(x[1], y[1]))
        
        self.filters_list = [["blk", "-- Filters --"]]
        self.filters_list += sorted_filters
        self.filters_list += [["blk", '--Actions--'],["sh", 'Save as a Shortcut'],["sf", 'Save as a Filter'],["mf", 'Manage Filters']]
        
        self.middle_string = []
        for item in (['ilike', _('contains')], ['not ilike', _('doesn\'t contain')], ['=', _('is equal to')], 
                     ['<>', _('is not equal to')], ['>', _('greater than')], ['<', _('less than')], 
                     ['in', _('in')], ['not in', _('not in')]):
            self.middle_string += [item]
            
    def parse(self, model=None, root=None, fields=None, values={}):
        
        views = []
        search_model = model
        for node in root.childNodes:
            
            if not node.nodeType==node.ELEMENT_NODE:
                continue
            
            filter_attrs = {}
            attrs = tools.node_attributes(node)
            attrs['label_position'] = 'True'
            attrs['model'] = search_model
            
            if attrs.has_key('colspan'):
                attrs['colspan'] = 1

            if attrs.has_key('nolabel'):
                attrs['nolabel'] = False
                
            if node.localName in ('form', 'tree'):
                n = self.parse(model=search_model, root=node, fields=fields, values=values)
                views += [Frame(children=n, **attrs)]

            elif node.localName in ('notebook', 'page'):
                n = self.parse(model=search_model, root=node, fields=fields, values=values)
                views += [Frame(children=n, **attrs)]

            elif node.localName == 'search':
                n = self.parse(model=search_model, root=node, fields=fields, values=values)
                views += [Frame(children=n, **attrs)]

            elif node.localName=='group':
                n = self.parse(model=search_model, root=node, fields=fields, values=values)
                views += [Group(children=n, **attrs)]
                
            elif node.localName=='newline':
                views += [NewLine(**attrs)]
                    
            elif node.localName=='filter':
                kind = 'filter'
                attrs['model'] = search_model
                field = FILTER[kind](**attrs)
                
                views += [field]
            
#            elif node.localName=='separator':
#                kind = 'separator'
#                field = WIDGETS[kind](**attrs)
#                
#                views += [field]
           
            elif node.localName == 'field':
                name = attrs['name']
                filter_field = {}
                
                if name in self.fields_type:
                    continue
                
                # If search view available then select=1 wont consider. All fields will display from search view.
                if not ('select' in attrs or 'select' in fields[name]):
                    continue
              
                if attrs.get('widget', False):
                    if attrs['widget']=='one2many_list':
                        attrs['widget']='one2many'
                    if attrs['widget']=='selection':
                        attrs['widget']='selection'
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

                if kind == 'boolean':
                    field.options = [[1, 'Yes'],[0, 'No']]
                    field.validator.if_empty = ''

                if values.has_key(name) and isinstance(field, (TinyInputWidget, RangeWidget)):
                    field.set_value(values[name])
                
                if field:
                    views += [field]
                
                for n in node.childNodes:
                    if n.localName=='filter':
                        attrs = tools.node_attributes(n)
                        kind = 'filter'
                        
                        filter_field = FILTER[kind](**attrs)
                        filter_field.onchange = None
                        filter_field.callback = None
                        
                        views += [filter_field]
                
        return views

RANGE_WIDGETS = {
    'date': DateTime,
    'time': DateTime,
    'datetime': DateTime,
    'float': Float,
    'integer': Integer,
}

FILTER = {
    'filter': Filter
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
    'separator': Separator
}

# vim: ts=4 sts=4 sw=4 si et
