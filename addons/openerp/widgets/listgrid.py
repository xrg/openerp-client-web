###############################################################################
#
#  Copyright (C) 2007-TODAY OpenERP SA. All Rights Reserved.
#
#  $Id$
#
#  Developed by OpenERP (http://openerp.com) and Axelor (http://axelor.com).
#
#  The OpenERP web client is distributed under the "OpenERP Public License".
#  It's based on Mozilla Public License Version (MPL) 1.1 with following 
#  restrictions:
#
#  -   All names, links and logos of OpenERP must be kept as in original
#      distribution without any changes in all software screens, especially
#      in start-up page and the software header, even if the application
#      source code has been changed or updated or code has been added.
#
#  You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################
import copy
import math
import xml.dom.minidom
import re
from openerp import utils
from itertools import chain, count

import cherrypy
from openerp.utils import rpc, icons, common, expr_eval, node_attributes
from openerp.widgets import TinyWidget, TinyInputWidget, ConcurrencyInfo, get_widget

import form
from openobject import tools
from openobject.tools import ast
from openobject.i18n import format
from pager import Pager


class List(TinyWidget):

    template = "/openerp/widgets/templates/listgrid/listgrid.mako"
    params = ['name', 'data', 'columns', 'headers', 'model', 'selectable', 'editable',
              'pageable', 'selector', 'source', 'offset', 'limit', 'show_links', 'editors', 'view_mode',
              'hiddens', 'edit_inline', 'field_total', 'link', 'checkbox_name', 'm2m', 'min_rows', 'string', 'o2m', 'dashboard', 'impex']

    member_widgets = ['pager', 'buttons', 'editors', 'concurrency_info']

    pager = None
    field_total = {}
    editors = {}
    hiddens = []
    buttons = []

    edit_inline = None
    data = None
    columns = 0
    headers = None
    model = None
    selectable = False
    editable = False
    pageable = False
    show_links = 1
    source = None
    checkbox_name = True
    min_rows = 5

    def __init__(self, name, model, view, ids=[], domain=[], context={}, **kw):

        super(List, self).__init__(name=name, model=model, ids=ids)
        
        self.context = context or {}
        self.domain = domain or []
        custom_search_domain = getattr(cherrypy.request, 'custom_search_domain', [])
        custom_filter_domain = getattr(cherrypy.request, 'custom_filter_domain', [])

        if name.endswith('/'):
            self._name = name[:-1]
        if name != '_terp_list':
            self.source = self.name.replace('/', '/') or None
        
        self.sort_order = ''
        self.sort_key = ''
        #this Condition is for Dashboard to avoid new, edit, delete operation
        self.dashboard = 0
        
        self.selectable = kw.get('selectable', 0)
        self.editable = kw.get('editable', False)
        self.pageable = kw.get('pageable', True)
        self.view_mode = kw.get('view_mode', [])
        
        self.offset = kw.get('offset', 0)
        self.limit = kw.get('limit', 0)
        self.count = kw.get('count', 0)
        self.link = kw.get('nolinks')
        self.m2m = kw.get('m2m', 0)
        self.o2m = kw.get('o2m', 0)
        self.concurrency_info = None
        self.selector = None

        terp_params = getattr(cherrypy.request, 'terp_params', {})
        if terp_params:
            if terp_params.get('_terp_model'):
                if terp_params['_terp_model'] == 'board.board' and terp_params.view_type == 'form':
                    self.dashboard = 1
            if terp_params.get('_terp_source'):
                if (str(terp_params.source) == self.source) or (terp_params.source == '_terp_list' and terp_params.sort_key):
                    self.sort_key = terp_params.sort_key
                    self.sort_order = terp_params.sort_order
        
        if self.selectable == 1:
            self.selector = 'radio'

        if self.selectable == 2:
            self.selector = 'checkbox'

        fields = view['fields']
        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]

        attrs = node_attributes(root)
        self.string = attrs.get('string','')

        search_param = copy.deepcopy(domain) or []
        if custom_search_domain:
            for elem in custom_search_domain:
                if elem not in self.domain:
                    search_param.append(elem)
                    
            for elem in custom_filter_domain:
                if elem not in self.domain:
                    search_param.append(elem)

        try:
            self.limit = int(attrs.get('limit'))
        except:
            pass

        self.colors = {}
        for color_spec in attrs.get('colors', '').split(';'):
            if color_spec:
                colour, test = color_spec.split(':')
                self.colors[colour] = test

        proxy = rpc.RPCProxy(model)
        
        default_data = kw.get('default_data', [])
        search_text = terp_params.get('_terp_search_text', False)
        if not self.source:
            self.source = terp_params.get('_terp_source', None)
        if not default_data and not self.o2m and not self.m2m:
            if self.limit > 0:
                if self.sort_key:
                    ids = proxy.search(search_param, self.offset, self.limit, self.sort_key + ' ' +self.sort_order, context)
                else:
                    if search_text:
                        if self.source == '_terp_list':
                            ids = proxy.search(search_param, self.offset, self.limit, False, context)
                    else:
                        ids = proxy.search(search_param, self.offset, self.limit, False, context)
            else:
                ids = proxy.search(search_param, 0, 0, 0, context)
            if len(ids) < self.limit:
                if self.offset > 0:
                    self.count = len(ids) + self.offset
                else:
                    self.count = len(ids)
            else:
                self.count = proxy.search_count(search_param, context)

        self.data_dict = {}
        data = []

        if ids and not isinstance(ids, list):
            ids = [ids]

        if ids and len(ids) > 0:

            ctx = rpc.session.context.copy()
            ctx.update(context)
            
            try:    
                data = proxy.read(ids, fields.keys() + ['__last_update'], ctx)
            except:
                pass
            
            ConcurrencyInfo.update(self.model, data)
            self.concurrency_info = ConcurrencyInfo(self.model, ids)
            
            order_data = [(d['id'], d) for d in data]
            orderer = dict(zip(ids, count()))
            ordering = sorted(order_data, key=lambda object: orderer[object[0]])
            data = [i[1] for i in ordering]
            
            for item in data:
                self.data_dict[item['id']] = item.copy()

            self.ids = ids
        elif kw.get('default_data', []):
            data = kw['default_data']

        self.values = copy.deepcopy(data)
        self.headers, self.hiddens, self.data, self.field_total, self.buttons = self.parse(root, fields, data)

        for k, v in self.field_total.items():
            if(len([test[0] for test in self.hiddens if test[0] == k])) <= 0:
                self.field_total[k][1] = self.do_sum(self.data, k)

        self.columns = len(self.headers)

        self.columns += (self.selectable or 0) and 1
        self.columns += (self.editable or 0) and 2
        self.columns += (self.buttons or 0) and 1

        if self.pageable:
            self.pager = Pager(ids=self.ids, offset=self.offset, limit=self.limit, count=self.count)
            self.pager._name = self.name
           
        if self.editable and context.get('set_editable'):#Treeview editable by default or set_editable in context
            attrs['editable'] = "bottom"
        
        # make editors
        if self.editable and attrs.get('editable') in ('top', 'bottom'):

            for f, fa in self.headers:
                if not isinstance(fa, int):
                    fa['prefix'] = '_terp_listfields' + ((self.name != '_terp_list' or '') and '/' + self.name)
                    fa['inline'] = True
                    
                    Widget = get_widget(fa.get('type', 'char')) or get_widget('char')
                    self.editors[f] = Widget(**fa)

            # generate hidden fields
            for f, fa in self.hiddens:
                fa['prefix'] = '_terp_listfields' + ((self.name != '_terp_list' or '') and '/' + self.name)
                self.editors[f] = form.Hidden(**fa)

        # limit the data
        if self.pageable and len(self.data) > self.limit and self.limit != -1:
            self.data = self.data[self.offset:]
            self.data = self.data[:min(self.limit, len(self.data))]

    def do_sum(self, data, field):
        sum = 0.0

        for d in data:
            value = d[field].value
            sum += value

        attrs = {}
        if data:
            d = data[0]
            attrs = d[field].attrs

        digits = attrs.get('digits', (16,2))
        if isinstance(digits, basestring):
            digits = eval(digits)

        integer, digit = digits
        return format.format_decimal(sum or 0.0, digit)

    def display(self, value=None, **params):

        # set editor values
        if not (self.editors and self.edit_inline):
            return super(List, self).display(value, **params)

        ctx = dict(rpc.session.context,
                   **self.context)

        fields = [name for name, _ in chain(self.headers, self.hiddens)]

        proxy = rpc.RPCProxy(self.model)
        if self.edit_inline > 0 and isinstance(self.edit_inline, int) and \
                self.edit_inline in self.data_dict:
            values = self.data_dict[self.edit_inline]
        else:
            values = dict(proxy.default_get(fields, ctx))

            # update values according to domain
            for (field, operator, value) in self.domain:
                if field in fields:
                    if operator == '=':
                        values[field] = value
                    elif operator == 'in' and len(value) == 1:
                        values[field] = value[0]
                        
            #call on_change methods
            headers_index = dict([(item[0], item[1]) for item in self.headers])
            to_check = values.keys()
            for field_name in to_check:
                if not field_name in headers_index:
                    continue
                props = headers_index[field_name]
                if not "on_change" in props:
                    continue
                on_change_method = props["on_change"]
                
                match = re.match('^(.*?)\((.*)\)$', on_change_method)
                if not match:
                    raise common.error(_('Application Error'), _('Wrong on_change trigger'))
                func_name = match.group(1)
                arg_names = [n.strip() for n in match.group(2).split(',')]
                
                args = [values[arg] if arg in values else False for arg in arg_names]
                
                proxy = rpc.RPCProxy(self.model)
                response = getattr(proxy, func_name)([], *args)
                if response is False:
                    response = {}
                if 'value' not in response:
                    response['value'] = {}
                
                new_values = response["value"]
                for k, v in new_values.items():
                    if v not in values or values[k] != v:
                        values[k] = v

        for f in fields:
            if f in values:
                self.editors[f].set_value(values[f])

        return super(List, self).display(value, **params)

    def parse(self, root, fields, data=[]):
        """Parse the given node to generate valid list headers.

        @param root: the root node of the view
        @param fields: the fields

        @return: an instance of List
        """

        headers = []
        hiddens = []
        buttons = []
        field_total = {}
        values  = [row.copy() for row in data]

        myfields = [] # check for duplicate fields

        for node in root.childNodes:

            if node.nodeName == 'button':
                attrs = node_attributes(node)
                if attrs.get('invisible', False):
                    visible = eval(attrs['invisible'], {'context':self.context})
                    if visible:
                        continue
                buttons += [Button(**attrs)]
                headers.append(("button", len(buttons)))
                
            elif node.nodeName == 'field':
                attrs = node_attributes(node)

                if 'name' in attrs:

                    name = attrs['name']

                    if name in myfields:
                        print "-"*30
                        print " malformed view for:", self.model
                        print " duplicate field:", name
                        print "-"*30
                        raise common.error(_('Application Error'), _('Invalid view, duplicate field: %s') % name)

                    myfields.append(name)

                    if attrs.get('widget'):
                        if attrs['widget']=='one2many_list':
                            attrs['widget']='one2many'
                        attrs['type'] = attrs['widget']

                    try:
                        fields[name].update(attrs)
                    except:
                        print "-"*30,"\n malformed tag for:", attrs
                        print "-"*30
                        raise

                    kind = fields[name]['type']

                    if kind not in CELLTYPES:
                        kind = 'char'

                    fields[name].update(attrs)

                    try:
                        visval = fields[name].get('invisible', 'False')
                        invisible = eval(visval, {'context': self.context})
                    except NameError, e:
                        cherrypy.log.error(e, context='listgrid.List.parse')
                        invisible = False

                    if invisible:
                        hiddens += [(name, fields[name])]

                    if 'sum' in attrs:
                        field_total[name] = [attrs['sum'], 0.0]

                    for i, row in enumerate(data):

                        row_value = values[i]
                        if invisible:
                            cell = Hidden(**fields[name])
                            cell.set_value(row_value.get(name, False))
                        else:
                            cell = CELLTYPES[kind](value=row_value.get(name, False), **fields[name])

                        for color, expr in self.colors.items():
                            try:
                                if expr_eval(expr,
                                     dict(row_value, active_id=rpc.session.active_id or False)):
                                    cell.color = color
                                    break
                            except:
                                pass

                        row[name] = cell

                    if invisible:
                        continue

                    headers += [(name, fields[name])]

        return headers, hiddens, data, field_total, buttons

class Char(TinyWidget):
    template = "/openerp/widgets/templates/listgrid/char.mako"

    params = ['text', 'link', 'value']

    def __init__(self, **attrs):

        super(Char, self).__init__(**attrs)

        self.attrs = attrs.copy()

        self.text = self.get_text()
        self.link = self.get_link()

        self.color = None
        self.onclick = None

    def get_text(self):
        return self.value or ''

    def get_link(self):
        return None

    def get_sortable_text(self):
        """ If returns anything other then None, the return value will be
        used to sort the listgrid. Useful for localized data.
        """
        return None

    def __unicode__(self):
        return ustr(self.text)

    def __str__(self):
        return ustr(self.text)

class M2O(Char):

    def get_text(self):

        if isinstance(self.value, int):
            self.value = self.value, rpc.name_get(self.attrs['relation'], self.value, rpc.session.context)

        if self.value and len(self.value) > 0:
            if isinstance(self.value, (tuple, list)):
                return self.value[-1]
            else:
                return self.value

        return ''

    def get_link(self):
        m2o_link = int(self.attrs.get('link', 1))

        if m2o_link == 1:
            return tools.url('/openerp/form/view', model=self.attrs['relation'], id=(self.value or False) and self.value[0])
        else:
            return None

class O2M(Char):

    def get_text(self):
        return "(%d)" % len(self.value)

class M2M(Char):

    def get_text(self):
        return "(%d)" % len(self.value)

class Selection(Char):

    def get_text(self):
        if self.value:
            if isinstance(self.value, (tuple, list)):
                self.value = self.value[0]

            selection = self.attrs['selection']
            for k, v in selection:
                if k == self.value:
                    return v
        return ''

class Float(Char):

    def get_text(self):
        digits = self.attrs.get('digits', (16,2))
        if isinstance(digits, basestring):
            digits = eval(digits)

        integer, digit = digits
        return format.format_decimal(self.value or 0.0, digit)

    def get_sortable_text(self):
        return ustr(self.value or '0.0')

class FloatTime(Char):

    def get_text(self):
        val = self.value or 0.0
        t = '%02d:%02d' % (math.floor(abs(val)),round(abs(val)%1+0.01,2) * 60)
        
        hour, min = t.split(':')
        if int(min) == 60:
            t = str(int(hour) + 1) + ":00"
        if val < 0:
            t = '-' + t

        return t

class Int(Char):

    def get_text(self):
        if self.value:
            if isinstance(self.value, (unicode, str)):
                return ast.literal_eval(self.value)
            return int(self.value)

        return 0

class ProgressBar(Char):
    template = "/openerp/widgets/templates/listgrid/progressbar.mako"

    params = ['range']


    def get_text(self):
        if not self.value:
            return 0.0
        
        if isinstance(self.value, float):
            self.value = '%.2f' % (self.value)
            self.value = float(self.value)

            if self.value > 100.0:
                self.range = 100.0
            else:
                self.range = self.value
            return self.range
        else:
            self.value = '%d' % (self.value)
            self.range = self.value
            return self.range

class DateTime(Char):

    def get_text(self):
        return format.format_datetime(self.value, kind=self.attrs.get('type', 'datetime'))

    def get_sortable_text(self):
        return ustr(self.value or '')

class Boolean(Char):
    template = "/openerp/widgets/templates/listgrid/boolean.mako"

    params = ['val', 'kind']

    def get_text(self):
        self.val = int(self.value)
        self.kind = 'boolean'
#        if int(self.value) == 1:
#            return _('Yes')
#        else:
#            return _('No')

class Button(TinyInputWidget):

    params = ['icon', 'id', 'parent_grid', 'btype', 'confirm', 'width', 'context']

    template = "/openerp/widgets/templates/listgrid/button.mako"

    def __init__(self, **attrs):
        super(Button, self).__init__(**attrs)

        self.states = attrs.get('states')
        if self.states:
            self.states = self.states.split(',')

        self.btype = attrs.get('special', attrs.get('type', 'workflow'))
        self.icon = attrs.get('icon')
        self.attrs = attrs.get('attrs', {})
        if self.icon:
            self.icon = icons.get_icon(self.icon)

        self.context = attrs.get('context', {})

        self.help = self.help or self.string
        self.confirm = attrs.get('confirm') or ''
        self.readonly = False

        self.width = attrs.get('width', 16)

    def params_from(self, data):

        id = data.get('id')
        visible = True

        if self.states:
            state = data.get('state')
            try:
                state = ((state or False) and state.value) or 'draft'
            except:
                state = ustr(state)
            visible = state in self.states

        return dict(id=id, visible=visible)

    def update_params(self, params):
        super(Button, self).update_params(params)
        params['attrs']['attrs']=self.attrs

class Hidden(TinyInputWidget):
    template = "openerp/widgets/templates/listgrid/hidden.mako"

    params = ['relation', 'field_id']
    member_widgets = ['widget']

    def __init__(self, **attrs):
        super(Hidden, self).__init__(**attrs)
        kind = self.kind or 'text'
        self.widget = get_widget(kind)(**attrs)
        self.validator = self.widget.validator
        self.relation = attrs.get('relation') or None
        self.editable = self.readonly
        if 'field_id' not in attrs:
            self.field_id = self.name

    def set_value(self, value):
        self.widget.set_value(value)
        self.default = self.widget.default

    def get_sortable_text(self):
        """ If returns anything other then None, the return value will be
        used to sort the listgrid. Useful for localized data.
        """
        return None

    def update_params(self, params):
        super(Hidden, self).update_params(params)


CELLTYPES = {
        'char':Char,
        'many2one':M2O,
        'datetime':DateTime,
        'date':DateTime,
        'one2many':O2M,
        'many2many':M2M,
        'selection':Selection,
        'float':Float,
        'float_time':FloatTime,
        'integer':Int,
        'boolean' : Boolean,
        'progressbar' : ProgressBar
}
