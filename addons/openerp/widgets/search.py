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
import random
import xml.dom.minidom

import cherrypy
import copy
from openerp.utils import rpc, cache, icons, node_attributes, expr_eval
from openerp.widgets import TinyInputWidget
from openerp.widgets.form import Char, Frame, Float, DateTime, Integer, Selection, Notebook
from openerp.widgets.form import Separator, FiltersGroup, Group, NewLine, M2O

from openobject.widgets import JSLink, locations


def get_search_default(attrs={}, screen_context=None, default_domain=[]):

    flag = True
    if cherrypy.request.path_info == '/openerp/tree/open':
        flag = False

    screen_context = screen_context or {}
    default_domain = attrs.get('default_domain', default_domain)
    default_search = False

    default_val = attrs.get('default')
    if default_val:
        default_val = expr_eval(default_val, {'context':screen_context})

    if attrs.get('name', False):
        context_str = 'search_default_' + str(attrs['name'])
        default_search = screen_context.get(context_str, False)

    if flag:
        if default_domain and attrs.get('domain'):
            domain =  expr_eval(attrs.get('domain'))
            for d in domain:
                if d in default_domain:
                    default_val = default_search = True

                else:
                    default_val = default_search = False
        else:
            default_val = default_search =  False

        if attrs.get('context'):
            ctx =  expr_eval(attrs.get('context', "{}"), {'self':attrs.get('name', False)})
            if ctx.get('group_by'):
                str_ctx = 'group_' + ctx.get('group_by')
                default_val = str_ctx in screen_context.get('group_by', [])
                default_search = str_ctx in screen_context.get('group_by', [])
    return default_search or default_val

class RangeWidget(TinyInputWidget):
    template = "templates/rangewid.mako"

    params = ["field_value"]
    member_widgets = ["from_field", "to_field"]

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
        start = value.get('from', '')
        end = value.get('to', '')

        self.from_field.set_value(start)
        self.to_field.set_value(end)

class Filter(TinyInputWidget):
    template = "templates/filter.mako"

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

class M2O_search(M2O):
    template = """
        <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
                <td>
                    <input type="hidden" id="${name}" name="${name}" class="${css_class}" value="${value}"
                        ${py.attrs(attrs, kind=kind, domain=domain, context=ctx, relation=relation, m2o_filter_domain=filter_domain)}/>
                    <input type="text" id="${name}_text" class="${css_class}"
                        ${py.attrs(attrs, kind=kind, relation=relation, value=text, m2o_filter_domain=filter_domain)}/>
                    <input type="hidden" id="_hidden_${name}" value=""/>
                    <div id="autoCompleteResults_${name}" class="autoTextResults"></div>
                    % if error:
                        <span class="fielderror">${error}</span>
                    % endif
                </td>
                <td>
                    <img id="${name}_select" alt="${_('Search')}" title="${_('Search')}"
                        src="/openerp/static/images/fields-a-lookup-a.gif" class="${css_class} m2o_select"/>
                </td>
                <td class="item-image">
                    <img id="${name}_open" alt="${_('Open')}" title="${_('Open a resource')}"
                        src="/openerp/static/images/iconset-d-drop.gif" class="m2o_open"/>
                </td>
            </tr>
        </table>
        <script type="text/javascript">
            new ManyToOne('${name}');
        </script>
    """
    javascript = [JSLink("openerp", "javascript/m2o.js", location=locations.bodytop)]
    params = ['filter_domain']

    def __init__(self, **attrs):
        if attrs.get('default', False) == 'uid':
            attrs['default'] = rpc.session.uid

        filter_domain = None
        if attrs.get('filter_domain'):
            filter_domain = attrs['filter_domain']
        super(M2O_search, self).__init__(**attrs)

class Search(TinyInputWidget):
    template = "templates/search.mako"
    javascript = [JSLink("openerp", "javascript/search.js", location=locations.bodytop)]

    params = ['fields_type', 'filters_list', 'operators_map', 'fields_list', 'filter_domain']
    member_widgets = ['frame']

    _notebook = Notebook(name="search_notebook")

    def __init__(self, model, domain=None, context=None, values={}, filter_domain=None, search_view=None, group_by_ctx=[]):

        super(Search, self).__init__(model=model)

        self.domain = copy.deepcopy(domain) or []
        self.listof_domain = domain or []
        self.filter_domain = filter_domain or []
        self.custom_filter_domain = []
        self.context = context or {}
        self.search_view = search_view or "{}"
        self.model = model
        self.groupby = []

        if group_by_ctx and isinstance(group_by_ctx, basestring):
            self.groupby += group_by_ctx.split(',')
        else:
            self.groupby = group_by_ctx

        if values == "undefined":
            values = {}

        ctx = dict(rpc.session.context, **self.context)

        view_id = ctx.get('search_view') or False
        if getattr(cherrypy.request,'terp_params') and not view_id:
            view_id = cherrypy.request.terp_params.get('_terp_view_id', False)

        if isinstance (self.search_view, basestring):
            self.search_view = eval(self.search_view)

        if not self.search_view:
            self.search_view = cache.fields_view_get(self.model, view_id, 'search', ctx, True)

        self.fields_list = []
        fields = self.search_view['fields']

        for k,v in fields.items():
            if v['type'] in ('many2one', 'char', 'float', 'integer', 'date',
                             'datetime', 'selection', 'many2many', 'boolean',
                             'one2many') and v.get('selectable',  False):
                self.fields_list.append((k, v['string'], v['type']))
        if self.fields_list:
            self.fields_list.sort(lambda x, y: cmp(x[1], y[1]))
        try:
            dom = xml.dom.minidom.parseString(self.search_view['arch'])
        except:
            dom = xml.dom.minidom.parseString(self.search_view['arch'].encode('utf-8'))

        self.view_type = dom.firstChild.localName
        self.string = dom.documentElement.getAttribute('string')

        self.fields_type = {}

        self.fields = fields
        dict_select = {'True':'1','False':'0','1':'1','0':'0'}
        all_field_ids =  rpc.session.execute('object', 'execute', 'ir.model.fields', 'search', [('model','=',str(model))])
        if len(fields) != len(all_field_ids):
            new_fields = []
            all_fields =  rpc.session.execute('object', 'execute', 'ir.model.fields', 'read', all_field_ids)
            for item in all_fields:
                new_fields.append(item)
            field_dict = {}
            for new_field in new_fields:
                if isinstance(new_field['select_level'],(str,unicode)):
                    new_field['select_level'] = eval(new_field['select_level'],dict_select)
                if isinstance(new_field['selectable'],(str,unicode)):
                    new_field['selectable'] = eval(new_field['selectable'],dict_select)

                field_dict[new_field['name']]= {'string': new_field['field_description'],
                                                'type' : new_field['ttype'],
                                                'select': new_field['select_level'],
                                                'name' : new_field['name'],
                                                'readonly': new_field['readonly'],
                                                'relation': new_field['relation'],
                                                'required': new_field['required'],
                                                'translate': new_field['translate'],
                                                'selectable': new_field['selectable']}
            self.fields.update(field_dict)

        self.frame = self.parse(model, dom, self.fields, values)[0]

        my_acts = rpc.session.execute('object', 'execute', 'ir.filters', 'get_filters', model)

        sorted_filters = [(act.get('domain', act['id']), act['name'])
                          for act in my_acts]
        sorted_filters.sort(lambda x, y: cmp(x[1], y[1]))

        self.filters_list = [("blk", "-- Filters --")] \
                          + sorted_filters \
                          + [("blk", '--Actions--')]

        self.operators_map = [
            ('ilike', _('contains')), ('not ilike', _('doesn\'t contain')),
            ('=', _('is equal to')), ('<>', _('is not equal to')),
            ('>', _('greater than')), ('<', _('less than')),
            ('in', _('in')), ('not in', _('not in'))]

        if self.filter_domain == []:
            self.filter_domain += [(self.fields_list[0][0], self.operators_map[0][0], '')]
        else:
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
            attrs.update(label_position='True',
                         model=search_model)

            if 'nolabel' in attrs:
                attrs['nolabel'] = False

            if node.localName in ('form', 'tree', 'search', 'group'):
                if node.localName == 'group':
                    attrs['group_by_ctx'] = values.get('group_by_ctx')
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

                    if attrs.get('widget'):
                        if attrs['widget'] == 'one2many_list':
                            attrs['widget'] = 'one2many'
                        attrs['type'] = attrs['widget']


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

                    kind = fields[name]['type']

                    if kind not in WIDGETS:
                        continue

                    if kind == 'many2one':
                        attrs['relation'] = fields[name]['relation']
                        attrs['type'] = fields[name]['type']
                        string = attrs.get('string', None)
                        if not string:
                            attrs['string'] = fields[name]['string']

                    self.fields_type[name] = kind

                    field = WIDGETS[kind](**fields[name])
                    field.onchange = None
                    field.callback = None

                    if kind == 'boolean':
                        field.options = [(1, 'Yes'),(0, 'No')]
                        field.validator.if_empty = ''

                    default_search = None
                    if name:
                        default_search = get_search_default(fields[name], self.context, self.domain)
                        s = default_search or values.get(name)
                        if s:
                            domain = []
                            if attrs.get('filter_domain'):
                                domain = expr_eval(attrs['filter_domain'], {'self': s})
                            else:
                                if field.kind == 'char':
                                    domain = [(name,fields[name].get('comparator','ilike'), s)]
                                if field.kind == 'selection' or field.kind == 'many2one':
                                    domain = [(name, '=', s)]
                            field.set_value(s)
                            self.listof_domain += [i for i in domain if not i in self.listof_domain]
                            self.context.update(expr_eval(attrs.get('context',"{}"), {'self': s}))

                    if (not default_search) and name in values and isinstance(field, (TinyInputWidget, RangeWidget)):
                        field.set_value(values[name])

                    views.append(field)
                    if node.childNodes:
                        for n in node.childNodes:
                            if n.localName=='filter':
                                attrs_child = node_attributes(n)
                                attrs_child['default_domain'] = self.domain
                                attrs_child['screen_context'] = self.context
                                if attrs_child.get('string'):
                                    attrs_child['string'] = ''
                                if values and values.get('group_by_ctx'):
                                    attrs['group_by_ctx'] = values['group_by_ctx']
                                filter_field = Filter(**attrs_child)
                                filter_field.onchange = None
                                filter_field.callback = None
                                if filter_field.groupcontext and filter_field.groupcontext not in self.groupby:
                                    self.groupby.append(filter_field.groupcontext)
                                self.listof_domain += [i for i in filter_field.global_domain if not i in self.listof_domain]
                                views.append(filter_field)
        if filters_run:
            views.append(FiltersGroup(children=filters_run))
        return views

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

# vim: ts=4 sts=4 sw=4 si et
