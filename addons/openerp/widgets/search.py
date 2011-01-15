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
# -   All names, links and logos of Tiny, OpenERP and Axelor must be
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
import random
import xml.dom.minidom

import cherrypy
import copy

from openerp.utils import rpc, cache, icons, node_attributes, expr_eval
from openerp.widgets import TinyInputWidget, InputWidgetLabel, form

from openobject.widgets import JSLink, locations

from openobject.i18n.format import convert_date_format_in_domain


def get_search_default(attrs, screen_context=None, default_domain=[]):
    screen_context = screen_context or {}

    if 'context' in attrs:
        ctx = expr_eval(attrs.get('context', "{}"), {'self':attrs.get('name', False)})
        group_by = ctx.get('group_by')
        if group_by:
            if isinstance(group_by, list):
                str_ctx = map(lambda x: 'group_' + x, group_by)
            else:
                str_ctx = 'group_' + group_by
            result = str_ctx in screen_context.get('group_by', [])
            return  result or attrs.get('name') and screen_context.get('search_default_' + attrs.get('name'))

    if cherrypy.request.path_info != '/openerp/listgrid/get' and 'name' in attrs:
        search_default = screen_context.get('search_default_' + attrs['name'])
        if search_default:
            # The value of search_default_$field can be either a literal
            # (integer, string, ...) or the name of a search_default context
            # variable. Try .get()ing the value in case it's a context object,
            # otherwise return the literal itself
            # ...
            # or so I expected, apparently somebody else already did the
            # resolution of those, so either we have a truthy value and we
            # return it, or we don't and we don't do anything
            return search_default

    return False

class RangeWidgetLabel(InputWidgetLabel):
    template = '/openerp/widgets/templates/search/rangewid_label.mako'
class RangeWidget(TinyInputWidget):
    template = "/openerp/widgets/templates/search/rangewid.mako"

    params = ["field_value"]
    member_widgets = ["from_field", "to_field"]

    label_type = RangeWidgetLabel

    colspan=3

    def __init__(self, **attrs):
        super(RangeWidget, self).__init__(**attrs)

        kind = attrs.get('type', 'integer')

        fname = attrs['name']

        from_attrs = dict(attrs, name=fname+'/from')
        to_attrs = dict(attrs, name=fname+'/to')

        self.from_field = RANGE_WIDGETS[kind](**from_attrs)
        self.to_field = RANGE_WIDGETS[kind](**to_attrs)

        # in search view fields should be writable
        self.from_field.readonly = False
        self.to_field.readonly = False

        # register the validators
        if hasattr(cherrypy.request, 'terp_validators'):
            for widget in [self.from_field, self.to_field]:
                cherrypy.request.terp_validators[str(widget.name)] = widget.validator
                cherrypy.request.terp_fields += [widget]

    def set_value(self, value):

        if isinstance(value, basestring):
            start = value
            end = ''
        else:
            start = value.get('from', '')
            end = value.get('to', '')

        self.from_field.set_value(start)
        self.to_field.set_value(end)

class Filter(TinyInputWidget):
    template = "/openerp/widgets/templates/search/filter.mako"

    params = ['icon', 'filter_domain', 'help', 'filter_id', 'text_val', 'group_context', 'def_checked', 'filter_context']

    def __init__(self, **attrs):
        super(Filter, self).__init__(**attrs)

        default_domain = attrs.get('default_domain')
        self.global_domain = []
        self.icon = attrs.get('icon')
        self.filter_domain = attrs.get('domain', [])
        self.help = attrs.get('help')
        self.filter_id = 'filter_%s' % (random.randint(0,10000))
        filter_context = attrs.get('context')
        screen_context = attrs.get('screen_context', {})

        self.def_checked = False
        self.groupcontext = []

        default_search = get_search_default(attrs, screen_context, default_domain)

        # context implemented only for group_by.
        self.group_context = None
        if filter_context:
            self.filter_context = eval(filter_context)
            self.group_context = self.filter_context.get('group_by', False)
            if self.group_context:
                if isinstance(self.group_context, list):
                    self.group_context = map(lambda x: 'group_' + x, self.group_context)
                else:
                    self.group_context = 'group_' + self.group_context

        if default_search:
            self.def_checked = True
            self.global_domain += (expr_eval(self.filter_domain, {'context':screen_context}))
            if self.group_context:
                self.groupcontext = self.group_context

        self.nolabel = True
        self.readonly = False
        if self.filter_context:
            if not self.filter_context.get('group_by'):
                self.filter_context = self.filter_context
            else:
                self.filter_context = {}
        self.text_val = self.string or self.help
        if self.icon:
            self.icon = icons.get_icon(self.icon)

        if self.string == self.help:
            self.help = None

        self.first_box = attrs.get('first_box')
        self.last_box = attrs.get('last_box')
        self.first_last_box = attrs.get('first_last_box')
        
        if not self.def_checked and attrs.get('group_by_ctx'):
            if self.group_context in attrs['group_by_ctx']:
                self.def_checked = True
        
class M2O_search(form.M2O):
    template = "/openerp/widgets/templates/search/many2one.mako"
    def __init__(self, **attrs):
        attrs['m2o_filter_domain'] = attrs.get('filter_domain')

        super(M2O_search, self).__init__(**attrs)

class Search(TinyInputWidget):
    template = "/openerp/widgets/templates/search/search.mako"
    javascript = [JSLink("openerp", "javascript/search.js", location=locations.bodytop)]

    params = ['fields_type', 'filters_list', 'operators_map', 'fields_list', 'filter_domain', 'flt_domain', 'source']
    member_widgets = ['frame']

    def __init__(self, source, model, domain=None, context=None, values={}, filter_domain=None, search_view=None, group_by_ctx=[], **kw):
        super(Search, self).__init__(model=model)

        self.domain = copy.deepcopy(domain) or []
        self.listof_domain = domain or []
        self.filter_domain = filter_domain or []
        self.custom_filter_domain = []
        self.context = context or {}
        self.search_view = search_view or "{}"
        self.model = model
        self.groupby = []
        self.source = source
        if kw.get('clear'):
            self.source = None
        if group_by_ctx and isinstance(group_by_ctx, basestring):
            self.groupby += group_by_ctx.split(',')
        else:
            self.groupby = group_by_ctx

        if values == "undefined":
            values = {}

        ctx = dict(rpc.session.context, **self.context)
        if not self.groupby and (values and values.get('group_by_ctx')):
            self.groupby = values['group_by_ctx']
        
        view_id = kw.get('search_view_id', False)
        
            
        if isinstance (self.search_view, basestring):
            self.search_view = eval(self.search_view)

        if not self.search_view:
            self.search_view = cache.fields_view_get(self.model, view_id or False, 'search', ctx, True)

        self.fields_list = []
        fields = self.search_view['fields']

        self.domain = convert_date_format_in_domain(domain, fields, self.context)
        self.listof_domain = self.domain

        try:
            dom = xml.dom.minidom.parseString(self.search_view['arch'])
        except:
            dom = xml.dom.minidom.parseString(self.search_view['arch'].encode('utf-8'))

        self.view_type = dom.firstChild.localName
        self.string = dom.documentElement.getAttribute('string')

        self.fields_type = {}
        self.fields = fields
        all_fields = rpc.session.execute('object', 'execute', model, 'fields_get', rpc.session.context)
        if len(fields) != len(all_fields):
            common_fields = [f for f in all_fields if f in fields]
            for f in common_fields:
                del all_fields[f]
            field_dict = all_fields
            self.fields.update(field_dict)

        self.fields_list.extend((
            (field_name, ustr(field['string']), field['type'])
            for field_name, field in self.fields.iteritems()
            if field['type'] != 'binary'
            if field.get('selectable')
        ))

        if self.fields_list:
            self.fields_list.sort(lambda x, y: cmp(x[1], y[1]))

        self.frame = self.parse(model, dom, self.fields, values)
        if self.frame:
            self.frame = self.frame[0]

        my_acts = rpc.session.execute('object', 'execute', 'ir.filters', 'get_filters', model)

        sorted_filters = []
        for act in my_acts:
            action = [act['domain'], act['name']]
            act_ctx = eval(act['context'])
            if act_ctx and act_ctx.get('group_by'):
                action.append(ustr(act_ctx['group_by']))
            else:
                action.append("[]")
            action.append(act['id'])

            sorted_filters.append(action)
        sorted_filters.sort(lambda x, y: cmp(x[1], y[1]))

        self.filters_list = sorted_filters

        self.operators_map = [
            ('ilike', _('contains')), ('not ilike', _('doesn\'t contain')),
            ('=', _('is equal to')), ('<>', _('is not equal to')),
            ('>', _('greater than')), ('<', _('less than')),
            ('in', _('in')), ('not in', _('not in'))]

        self.flt_domain = str(self.filter_domain).replace("(", "[").replace(')', ']')
        self.custom_filter_domain = self.filter_domain

    def parse(self, model=None, root=None, fields=None, values={}):

        views = []
        search_model = model

        filters_run = []
        for node in root.childNodes:
            if not node.nodeType==node.ELEMENT_NODE:
                continue

            if filters_run and node.localName != 'filter':
                views.append(FiltersGroup(children=filters_run))
                filters_run = []

            attrs = node_attributes(node)
            attrs.update(is_search=True,
                         model=search_model)

            if 'nolabel' in attrs:
                attrs['nolabel'] = False

            if node.localName in ('form', 'tree', 'search', 'group'):
                if node.localName == 'group':
                    attrs['group_by_ctx'] = values.get('group_by_ctx')
                    attrs['expand'] = expr_eval(attrs.get('expand',False),{'context':self.context})
                    Element = Group
                else:
                    Element = Frame

                views.append(Element(children=
                                     self.parse(model=search_model, root=node,
                                                fields=fields, values=values),
                                     **attrs))

            elif node.localName=='newline':
                views.append(NewLine(**attrs))

            elif node.localName=='filter':
                attrs.update(
                    model=search_model,
                    default_domain=self.domain,
                    screen_context=self.context)
                if values and values.get('group_by_ctx'):
                    attrs['group_by_ctx'] = values['group_by_ctx']
                elif self.groupby:
                    attrs['group_by_ctx'] = self.groupby

                v = Filter(**attrs)
                if v.groupcontext and v.groupcontext not in self.groupby:
                    self.groupby.append(v.groupcontext)
                self.listof_domain.extend(i for i in v.global_domain if not i in self.listof_domain)
                filters_run.append(v)

            elif node.localName == 'field':
                val  = attrs.get('select', False) or fields[str(attrs['name'])].get('select', False) or self.view_type == 'search'
                if val:
                    name = attrs['name']
                    if name in self.fields_type:
                        continue

                    # in search view fields should be writable
                    attrs.update(readonly=False,
                                 required=False,
                                 translate=False,
                                 disabled=False,
                                 visible=True,
                                 invisible=False,
                                 editable=True,
                                 attrs=None)

                    try:
                        fields[name].update(attrs)
                    except:
                        print "-"*30,"\n malformed tag for:", attrs
                        print "-"*30
                        raise

                    if attrs.get('widget'):
                        if attrs['widget'] == 'one2many_list':
                            fields[name]['widget'] = 'one2many'

                        fields[name]['type2'] = fields[name]['type']
                        fields[name]['type'] = attrs['widget']

                    kind = fields[name]['type']

                    if kind not in WIDGETS:
                        continue

                    if kind == 'many2one':
                        attrs['relation'] = fields[name]['relation']
                        attrs['type'] = fields[name]['type']
                        if not attrs.get('string'):
                            attrs['string'] = fields[name]['string']

                    self.fields_type[name] = kind

                    field = WIDGETS[kind](**fields[name])
                    field.onchange = None
                    field.callback = None

                    if kind == 'boolean':
                        field.options = [[1,_('Yes')],[0,_('No')]]
                        field.validator.if_empty = ''

                    default_search = None
                    if name:
                        default_search = get_search_default(fields[name], self.context, self.domain)
                        defval = default_search
                        if defval:
                            model = fields[name].get('relation')
                            type2 = fields[name].get('type2')

                            if kind == 'many2one' and model:
                                try:
                                    value = rpc.name_get(model, default_search, self.context)
                                except Exception,e:
                                    value = defval
                                defval = value or ''

                            if attrs.get('filter_domain'):
                                domain = expr_eval(attrs['filter_domain'], {'self': defval})
                            else:
                                if field.kind == 'selection':
                                    domain = [(name, '=', int(defval) if type2 == 'many2one' else defval)]

                                elif field.kind in ('date','datetime'):
                                    domain = [(name, '>=', defval)]
                                    
                                elif field.kind == 'boolean':
                                    domain = [(name, '=', defval)]
                                               
                                else:
                                    domain = [(name,fields[name].get('comparator','ilike'), defval)]

                            field.set_value(defval)
                            self.listof_domain += [i for i in domain if not i in self.listof_domain]
                            self.context.update(expr_eval(attrs.get('context',"{}"), {'self': default_search}))

                    if (not default_search) and name in values and isinstance(field, TinyInputWidget):
                        field.set_value(values[name])

                    views.append(field)
                    for n in node.childNodes:
                        if n.localName=='filter':
                            attrs_child = dict(
                                node_attributes(n),
                                default_domain=self.domain,
                                screen_context=self.context)
                            if 'string' in attrs_child: del attrs_child['string']
                            if values and values.get('group_by_ctx'):
                                attrs['group_by_ctx'] = values['group_by_ctx']

                            filter_field = Filter(**attrs_child)
                            filter_field.onchange = None
                            filter_field.callback = None

                            if filter_field.groupcontext and filter_field.groupcontext not in self.groupby:
                                self.groupby.append(filter_field.groupcontext)
                            self.listof_domain.extend(i for i in filter_field.global_domain
                                                        if i not in self.listof_domain)
                            field.filters.append(filter_field)
        if filters_run:
            views.append(FiltersGroup(children=filters_run))
        return views

class FiltersGroup(form.Group):
    """ Special group for groups of *filters*, in order to generate
    the right markup and style the buttons correctly.
    """
    template = "/openerp/widgets/templates/search/filters_group.mako"
    colspan=1
    is_search = True
    def __init__(self, **attrs):
        attrs['is_search'] = True
        super(FiltersGroup, self).__init__(**attrs)

class Char(form.Char): pass
class DateTime(form.DateTime): pass
class Float(form.Float): pass
class Frame(form.Frame):
    def base_widget_attrs(self, widget, colspan, rowspan):
        attrs = super(Frame, self).base_widget_attrs(widget, colspan, rowspan)
        for key in ('colspan', 'rowspan', 'height', 'width'):
            if key in attrs: del attrs[key]
        return attrs

class Group(form.Group):
    def __init__(self, **attrs):
        super(Group, self).__init__(**attrs)
        self.frame = Frame(**attrs)

class Integer(form.Integer): pass
class NewLine(form.NewLine): pass
class Selection(form.Selection): pass
class Separator(form.Separator): pass

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
    'many2one': M2O_search,
    'email' : Char,
    'url' : Char,
    'separator': Separator
}
