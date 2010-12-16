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
import os
import random
import re
import xml.dom.minidom

import cherrypy
import simplejson
from openerp import validators
from openerp.utils import rpc, icons, common, TinyDict, node_attributes, get_node_xpath
from openerp.widgets import TinyWidget, TinyInputWidget, InputWidgetLabel, ConcurrencyInfo, get_widget, register_widget

from _binary import Image
from openobject import tools
from openobject.i18n import get_locale, format
from openobject.widgets import JSLink, locations


class Frame(TinyWidget):
    """Frame widget layouts the widgets in a table.
    """

    template = "/openerp/widgets/form/templates/frame.mako"

    params = ['table']
    member_widgets = ['hiddens', 'children']

    table = None

    def __init__(self, **attrs):

        super(Frame, self).__init__(**attrs)
        self.nolabel = True
        self.is_search = attrs.get('is_search', False)

        # In search view, there is no limit to the number of columns in a row
        # newlines have to be created explicitly
        if self.is_search:
            self.columns = None
        else:
            self.columns = int(attrs.get('col', 4))

        self.x = 0
        self.y = 0

        self.hiddens = []
        self.table = []

        self.add_row()

        for child in self.children:

            string = not child.nolabel and child.string
            rowspan = child.rowspan or 1
            colspan = child.colspan or 1
            if isinstance(child, NewLine):
                self.add_row()

            elif getattr(child, 'invisible', False):
                self.add_hidden(child)

            elif getattr(child, 'visible', True) or isinstance(child, (Button, Group, Page)):
                self.add(child, string, rowspan, colspan)

            elif isinstance(child, TinyInputWidget):
                self.add_hidden(child)


        if self.is_search:
            self.fix_group_colspans()

    def add_row(self):

        if len(self.table) and len(self.table[-1]) == 0:
            return self.table[-1]

        self.table.append([])

        self.x = 0
        self.y += 1

        return self.table[-1]

    def _add_validator(self, widget):

        if not isinstance(widget, TinyInputWidget) or \
                not widget.name or widget.readonly or \
                widget.name.startswith('_terp_listfields'):
            return

        if widget.validator:
            cherrypy.request.terp_validators[str(widget.name)] = widget.validator
            cherrypy.request.terp_fields.append(widget)

    def base_widget_attrs(self, widget, colspan, rowspan):
        attrs = {'for': widget.name}

        if isinstance(widget, TinyInputWidget):
            attrs['class'] = 'item'
        if rowspan > 1: attrs['rowspan'] = rowspan
        if colspan > 1: attrs['colspan'] = colspan
        if hasattr(widget, 'height'):
            attrs['height'] = widget.height
        if hasattr(widget, 'width'):
            attrs['width'] = widget.width

        return attrs

    def add(self, widget, label=None, rowspan=1, colspan=1):
        if self.columns and colspan > self.columns:
            colspan = self.columns

        label_size = label and 1 or 0

        if label_size == 1 and colspan == 2:
            colspan = 1

        if self.columns and colspan + self.x + label_size > self.columns:
            self.add_row()

        tr = self.table[-1]
        label_table = []
        if label:
            if colspan > 1:
                colspan -= 1
            attrs = {
                'class': 'label',
                'kind': getattr(widget, 'kind', None),
                'title': getattr(widget, 'help', None),
                'for': widget.name,
                'model': getattr(widget, 'model', None),
                'fname':getattr(widget, 'name', None),
                'widget_item': ({}, widget)
            }
            td = [attrs, label]

            if self.is_search:
                if colspan > 1:
                    attrs['colspan'] = colspan
                if getattr(widget, 'full_name', None):
                    attrs['class'] = attrs.get('class', 'label') + ' search_filters search_fields'
                    label_table = td
            else:
                attrs['width'] = '1%'
            tr.append(td)

        if isinstance(widget, TinyInputWidget) and hasattr(cherrypy.request, 'terp_validators'):
            self._add_validator(widget)

        attrs = self.base_widget_attrs(widget, colspan, rowspan)

        if not hasattr(widget, 'visible'):
            widget.visible = True

        # state change
        if getattr(widget, 'states', None):
            states = widget.states
            # convert into JS
            if isinstance(states, dict):
                states = dict([(k, dict(v)) for k, v in states.iteritems()])

            attrs.update(states=simplejson.dumps(states),
                         widget=widget.name)
            if not widget.visible:
                attrs['style'] = 'display: none'
            widget.visible = True

        if getattr(widget, "valign", None):
            attrs['valign'] = widget.valign

        # attr change
        if getattr(widget, 'attributes', None):
            attrs['attrs'] = str(widget.attributes)
            attrs['widget'] = widget.name

        if not isinstance(widget, (Char, Frame, Float, DateTime, Integer, Selection, Notebook, Separator, NewLine, Label)):
            from openerp.widgets.search import Filter
            if self.is_search \
               and (not (getattr(widget, 'kind', None) or widget._name)) \
               or (isinstance(widget, Filter) and widget.string):
                classes = [attrs.get('class', 'item'), 'search_filters']
                if isinstance(widget, Filter):
                    classes.append('group_box')
                    if widget.def_checked:
                        classes.append('grop_box_active')

                attrs['class'] = ' '.join(classes)
                attrs['nowrap'] = 'nowrap'

        attrs['class'] = attrs.get('class', '') + ' item-%s' % widget.__class__.__name__.lower()
        if self.columns and not attrs.has_key('width'):
            if label:
                attrs['width'] = str((100 / self.columns) * (colspan + 1) - 1) + '%'
            else:
                attrs['width'] = str((100 / self.columns) * colspan) + '%'

        td = [attrs, widget]
        if getattr(widget, 'full_name', None) and self.is_search and label_table:
            label_table[0]['widget_item'] = td
            label_table[0]['is_search'] = True
        else:
            tr.append(td)

        self.x += colspan + label_size

    def add_hidden(self, widget):
        if isinstance(widget, TinyInputWidget) and hasattr(cherrypy.request, 'terp_validators'):
            self._add_validator(widget)
        self.hiddens.append(widget)

    def fix_group_colspans(self):
        """ Colspans in search view are currently broken.

        If we're in search view, try to massage group colspans so they take 100% when alone on a row
        """
        # TODO: handle rowspans correctly
        max_colspan = max([
            reduce(lambda total, widget: total + widget[0].get('colspan', 1), row, 0)
            for row in self.table
        ])
        for row in self.table:
            if len(row) == 1:
                [(attrs, widget)] = row
                if isinstance(widget, Group):
                    attrs['colspan'] = max_colspan

class Notebook(TinyWidget):
    """Notebook widget, contains list of frames. Each frame will be displayed as a
    page of the the Notebook.
    """

    template = "/openerp/widgets/form/templates/notebook.mako"
    javascript = [JSLink("openerp", "javascript/notebook/notebook.js")]

    params = ['fake_widget']
    member_widgets = ['children']

    valign = "top"

    def __init__(self, **attrs):
        super(Notebook, self).__init__(**attrs)
        self.nolabel = True
        self.colspan = attrs.get('colspan', 3)

        self.fake_widget = '_fake'
        if attrs.get('prefix'):
            self.fake_widget = attrs['prefix'] + '/_fake'

register_widget(Notebook, ["notebook"])

class Page(Frame):

    def __init__(self, **attrs):
        super(Page, self).__init__(**attrs)
        if self.invisible:
            self.attributes = "{'invisible': [1]}"

register_widget(Page, ["page"])


class Separator(TinyWidget):
    """Separator widget.
    """

    template = "/openerp/widgets/form/templates/separator.mako"
    params = ["orientation"]

    def get_default_colspan(self):
        if self.orientation == 'horizontal':
            return 4
        else:
            return 1

    def __init__(self, **attrs):
        super(Separator, self).__init__(**attrs)
        self.orientation = attrs.get('orientation', 'horizontal')
        self.colspan = int(attrs.get('colspan', self.get_default_colspan()))
        self.rowspan = int(attrs.get('rowspan', 1))
        self.nolabel = True
        if self.orientation == 'vertical':
            self.width = 1

register_widget(Separator, ["separator"])


class NewLine(TinyWidget):
    """NewLine widget just tells the Frame widget to start new row during
    layout process.
    """
    template = "/openerp/widgets/form/templates/newline.mako"

register_widget(NewLine, ["newline"])


class Label(TinyWidget):

    template = "/openerp/widgets/form/templates/label.mako"

    params = ["field_value", "align"]

    def __init__(self, **attrs):
        super(Label, self).__init__(**attrs)

        self.nolabel = True
        self.field_value = self.string
        self.align = 'center'

        align = attrs.get('align', 0.5)
        if isinstance(align, basestring):
            try:
                align = eval(align)
            except:
                align = 0.5

        if align == 0.0:
            self.align = 'left'
        if align == 0.5:
            self.align = 'center'
        if align == 1.0:
            self.align = 'right'

    def set_value(self, value):
        self.field_value = unicode(value or '', 'utf-8')

register_widget(Label, ["label"])


class Char(TinyInputWidget):

    template = "/openerp/widgets/form/templates/char.mako"
    params = ['password', 'size']

    def __init__(self, **attrs):

        if attrs.get('password'):
            attrs.pop('invisible', None)

        super(Char, self).__init__(**attrs)
        self.validator = validators.String()

    def set_value(self, value):
        self.default = value

register_widget(Char, ["char"])


class Email(TinyInputWidget):
    template = "/openerp/widgets/form/templates/email.mako"

    def __init__(self, **attrs):
        super(Email, self).__init__(**attrs)
        self.validator = validators.Email()

    def set_value(self, value):
        if value:
            self.default = value

register_widget(Email, ["email"])


class Text(TinyInputWidget):
    template = "/openerp/widgets/form/templates/text.mako"

    def __init__(self, **attrs):
        super(Text, self).__init__(**attrs)
        self.validator = validators.String()

    def set_value(self, value):
        self.default = value

register_widget(Text, ["text", "text_tag"])


class Integer(TinyInputWidget):
    template = "/openerp/widgets/form/templates/integer.mako"

    def __init__(self, **attrs):
        super(Integer, self).__init__(**attrs)
        self.validator = validators.Int()

    def set_value(self, value):
        self.default = value or 0

register_widget(Integer, ["integer"])

class BooleanLabel(InputWidgetLabel):
    template = "/openerp/widgets/form/templates/boolean_label.mako"
class Boolean(TinyInputWidget):
    template = "/openerp/widgets/form/templates/boolean.mako"

    label_type = BooleanLabel

    def __init__(self, **attrs):
        super(Boolean, self).__init__(**attrs)
        self.validator = validators.Bool()

    def set_value(self, value):
        self.default = value or ''

register_widget(Boolean, ["boolean"])


class Float(TinyInputWidget):
    template = "/openerp/widgets/form/templates/float.mako"

    def __init__(self, **attrs):
        super(Float, self).__init__(**attrs)

        digits = attrs.get('digits', (16,2))
        if isinstance(digits, basestring):
            digits = eval(digits)

        integer, digit = digits

        self.validator = validators.Float(digit=digit)

#        if not self.default:
#            self.default = 0.0

    def set_value(self, value):
        self.default = value or 0.0

register_widget(Float, ["float"])


class FloatTime(TinyInputWidget):
    template = "/openerp/widgets/form/templates/floattime.mako"

    def __init__(self, **attrs):
        super(FloatTime, self).__init__(**attrs)
        self.validator = validators.FloatTime()

    def set_value(self, value):
        self.default = value

register_widget(FloatTime, ["float_time"])


class ProgressBar(TinyInputWidget):
    template = "/openerp/widgets/form/templates/progressbar.mako"

    def __init__(self, **attrs):
        super(ProgressBar, self).__init__(**attrs)

        if attrs.get('type2') == 'float':
            self.validator = validators.Float()
        else:
            self.validator = validators.Int()

    def set_value(self, value):
        self.default = value or 0.00

register_widget(ProgressBar, ["progressbar"])


class Selection(TinyInputWidget):
    template = "/openerp/widgets/form/templates/selection.mako"

    params = ['options', 'search_context', 'type2', 'operator']
    options = []
    search_context = {}

    def __init__(self, **attrs):
        super(Selection, self).__init__(**attrs)

        self.options = attrs.get('selection', [])
        self.type2 = attrs.get('type2')
        self.operator = attrs.get('operator', '=')
        # m2o as selection
        if not self.options and attrs.get('relation') and attrs.get('widget') == 'selection':
            proxy = rpc.RPCProxy(attrs['relation'])
            try:
                domain = attrs.get('domain', [])
                if isinstance(domain, (str, unicode)):
                    try:
                        domain = eval(domain)
                    except:
                        domain = []
                ids = proxy.search(domain)
                ctx = rpc.session.context.copy()
                self.search_context = attrs.get('context', {})
#                ctx.update(attrs.get('context', {})) # In search view this will create problem for m2o field having widget='selection' and context as attr.
                self.options = proxy.name_get(ids, ctx)
            except:
                self.options = []

        if self.options and self.options[0][0] == '' and isinstance(self.options[0][0], unicode):
            self.validator = validators.Selection()
        # determine the actual type
        elif self.options and isinstance(self.options[0][0], basestring):
            self.kind = 'char'
            self.validator = validators.String()
        else:
            self.validator = validators.Selection()

    def update_params(self, params):
        super(Selection, self).update_params(params)

        if self.search_context:
            params.setdefault('css_classes', []).append('selection_search')

    def set_value(self, value):

        if not value:
            value=''

        if isinstance(value, (tuple, list)):
            value = value[0]

        for s in dict(self.options):
            if str(s) == str(value):
                value = s

        super(Selection, self).set_value(value)

register_widget(Selection, ["selection"])


class DTLink(JSLink):

    def update_params(self, params):
        super(DTLink, self).update_params(params)

        locale = get_locale()
        link = "jscal/lang/calendar-%s.js" % locale

        if tools.resources.resource_exists("openerp", "static", link):
            params['link'] = tools.url(["/openerp/static", link])
        else:
            lang = locale.language
            link = "jscal/lang/calendar-%s.js" % lang
            if tools.resources.resource_exists("openerp", "static", link):
                params['link'] = tools.url(["/openerp/static", link])

class DateTime(TinyInputWidget):

    template = "/openerp/widgets/form/templates/datetime.mako"

    javascript = [DTLink("openerp", "jscal/lang/calendar-en.js", location=locations.bodytop)]

    params = ["format", "picker_shows_time"]

    format = '%Y-%m-%d %H:%M:%S'
    picker_shows_time = True

    def __init__(self, **attrs):
        super(DateTime, self).__init__(**attrs)
        self.format = format.get_datetime_format(attrs['type'])

        if attrs['type'] == 'date':
            self.picker_shows_time = False

        self.validator = validators.DateTime(kind=attrs['type'])

    def set_value(self, value):
        super(DateTime, self).set_value(value or False)

register_widget(DateTime, ["date", "time", "datetime"])


class URL(TinyInputWidget):
    template = "/openerp/widgets/form/templates/url.mako"

    def __init__(self, **attrs):
        super(URL, self).__init__(**attrs)
        self.validator = validators.URL()

    def set_value(self, value):
        if value:
            super(URL, self).set_value(value)

register_widget(URL, ["url"])


class Hidden(TinyInputWidget):
    template = "/openerp/widgets/form/templates/hidden.mako"

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

class Button(TinyInputWidget):

    template = "/openerp/widgets/form/templates/button.mako"
    params = ["btype", "id", "confirm", "icon", "target", "context", "default_focus"]

    visible = True
    def __init__(self, **attrs):
        super(Button, self).__init__(**attrs)

        # remove mnemonic
        self.string = re.sub('_(?!_)', '', self.string or '')

        self.btype = attrs.get('special', attrs.get('type', 'workflow'))
        self.context = attrs.get("context", {})
        self.nolabel = True
        self.target = ''
        if self.icon:
            self.icon = icons.get_icon(self.icon)
        self.default_focus = attrs.get('default_focus', 0)

    def set_state(self, state):
        if self.states:
            self.visible = state in self.states

register_widget(Button, ["button"])


class Group(TinyWidget):

    template = "/openerp/widgets/form/templates/group.mako"
    params = ["expand_grp_id", "default", "view_type", "states"]
    member_widgets = ["frame"]
    valign = "top"
    colspan = 4
    col = 4
    states = None
    visible = True

    def __init__(self, **attrs):
        super(Group, self).__init__(**attrs)

        if isinstance(self.states, basestring):
            self.states = self.states.split(',')
        self.set_state(attrs.get('state', 'draft'))

        self.default = int(attrs.get('expand', 0))
        self.frame = Frame(**attrs)
        self.nolabel = True
        self.view_type = cherrypy.request.terp_params.get('_terp_view_type')

        if attrs.get('group_by_ctx'):
            self.default = 1
        self.expand_grp_id = 'expand_grp_%s' % (random.randint(0,10000))

    def set_state(self, state):
        if self.states:
            self.visible = state in self.states

register_widget(Group, ["group"])

class Dashbar(TinyWidget):

    template = "/openerp/widgets/form/templates/dashbar.mako"

    javascript = [JSLink("openerp", "javascript/dashboard.js")]

    member_widgets = ['children']

register_widget(Dashbar, ["dashbar"])


class HPaned(TinyWidget):
    template = "/openerp/widgets/form/templates/hpaned.mako"

    member_widgets = ['children']

    def __init__(self, **attrs):
        super(HPaned, self).__init__(**attrs)
        self.nolabel = True

register_widget(HPaned, ["hpaned"])


class VPaned(TinyWidget):

    template = "/openerp/widgets/form/templates/vpaned.mako"

    member_widgets = ['children']

    def __init__(self, **attrs):
        super(VPaned, self).__init__(**attrs)
        self.nolabel = True

register_widget(VPaned, ["vpaned"])

class HtmlView(TinyWidget):

    template = "/openerp/widgets/form/templates/htmlview.mako"

    params = ['tag_name', 'args']
    member_widgets = ['children', 'frame']

    def __init__(self, **attrs):
        super(HtmlView, self).__init__(**attrs)
        self.tag_name = attrs.get('tag_name')

        self.args = attrs.get('args', {})

        if attrs.get('value'):
            self.default = attrs.get('value')

register_widget(HtmlView, ["html"])

class Form(TinyInputWidget):
    """A generic form widget
    """

    template = "/openerp/widgets/form/templates/form.mako"

    params = ['id']
    member_widgets = ['frame', 'concurrency_info']

    def __init__(self, prefix, model, view, ids=[], domain=[], context=None, editable=True, readonly=False, nodefault=False, nolinks=1):

        super(Form, self).__init__(prefix=prefix, model=model, editable=editable, readonly=readonly, nodefault=nodefault)
        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]
        attrs = node_attributes(root)
        fields = view['fields']
        self.string = attrs.get('string', '')
        self.link = attrs.get('link', nolinks)

        self.id = None

        proxy = rpc.RPCProxy(model)

        self.context = dict(rpc.session.context,
                                **(context or {}))
        self.context['bin_size'] = True

        values = {}
        defaults = {}

        # update values according to domain
        for d in domain:
            if d[0] in fields:
                if d[1] == '=':
                    values[d[0]] = d[2]
                if d[1] == 'in' and len(d[2]) == 1:
                    values[d[0]] = d[2][0]

        if ids:
            lval = proxy.read(ids[:1], fields.keys() + ['__last_update'], self.context)
            if lval:
                values = lval[0]
                self.id = ids[0]
                ConcurrencyInfo.update(self.model, [values])

        elif 'datas' in view: # wizard data

            for f in fields:
                if 'value' in fields[f]:
                    values[f] = fields[f]['value']

            values.update(view['datas'])

        elif not self.nodefault: # default
            try:
                defaults = proxy.default_get(fields.keys(), self.context)
            except:
                pass

        elif 'state' in fields: # if nodefault and state get state only
            defaults = proxy.default_get(['state'], self.context)

        elif 'x_state' in fields: # if nodefault and x_state get x_state only (for custom objects)
            defaults = proxy.default_get(['x_state'], self.context)

        for k, v in defaults.items():
            values.setdefault(k, v)

        self.state = values.get('state', values.get('x_state'))

        # store current record values in request object (see, self.parse & O2M default_get_ctx)
        if not hasattr(cherrypy.request, 'terp_record'):
            cherrypy.request.terp_record = TinyDict()

        self.view_fields = []
        self.nb_couter = 0
        self.frame = self.parse(prefix, dom, fields, values)[0]
        self.values = [values]
        self.concurrency_info = ConcurrencyInfo(self.model, [self.id])

        # We should generate hidden fields for fields which are not in view, as
        # the values of such fields might be used during `onchange`
        for name, attrs in fields.items():
            if name not in self.view_fields:

                kind = attrs.get('type', 'char')
                if not get_widget(kind):
                    continue

                attrs['prefix'] = prefix
                attrs['name'] = name
                attrs['readonly'] = True # always make them readonly

                field = self._make_field_widget(attrs, values.get(name))
                self.frame.add_hidden(field)

    def parse(self, prefix='', root=None, fields=None, values={}):

        views = []

        for node in root.childNodes:

            if node.nodeType not in (node.ELEMENT_NODE, node.TEXT_NODE):
                continue

            attrs = node_attributes(node)
            attrs['prefix'] = prefix
            attrs['state'] = self.state

            if node.localName=='image':
                views.append(Image(**attrs))

            elif node.localName=='separator':
                views.append(Separator(**attrs))

            elif node.localName=='label':
                text = attrs.get('string', '')

                if not text:
                    for node in node.childNodes:
                        if node.nodeType == node.TEXT_NODE:
                            text += node.data
                        else:
                            text += node.toxml()

                attrs['string'] = text
                views.append(Label(**attrs))

            elif node.localName=='newline':
                views.append(NewLine(**attrs))

            elif node.localName=='button':
                attrs['editable'] = self.editable
                views.append(Button(model=self.model, id=self.id, **attrs))

            elif node.localName == 'form':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views.append(Frame(children=n, **attrs))

            elif node.localName == 'notebook':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                nb = Notebook(children=n, **attrs)
                self.nb_couter += 1
                nb._name = prefix.replace('/', '_') + '_notebook_%s'  % (self.nb_couter)
                views.append(nb)

            elif node.localName == 'page':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views.append(Page(children=n, **attrs))

            elif node.localName=='group':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views.append(Group(children=n, **attrs))

            elif node.localName == 'field':
                name = attrs['name']

                try:
                    fields[name]['link'] = attrs.get('link', '1')
                    fields[name].update(attrs)
                except:
                    print "-"*30,"\n malformed tag for:", attrs
                    print "-"*30
                    raise

                kind = fields[name]['type']

                if not get_widget(kind):
                    continue

                if name in self.view_fields:
                    print "-"*30
                    print " malformed view for:", self.model
                    print " duplicate field:", name
                    print "-"*30
                    raise common.error(_('Application Error'), _('Invalid view, duplicate field: %s') % name)

                self.view_fields.append(name)

                field = self._make_field_widget(fields[name], values.get(name))
                views.append(field)

            elif node.localName=='hpaned':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views.append(HPaned(children=n, **attrs))

            elif node.localName=='vpaned':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views.append(VPaned(children=n, **attrs))

            elif node.localName in ('child1', 'child2'):
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                attrs['name'] = get_node_xpath(node)
                views.append(Dashbar(children=n, **attrs))

            elif node.localName=='action':
                wid = get_widget('action')(**attrs)
                views.append(wid)
                cherrypy.request._terp_dashboard = True

            else:
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                args = node_attributes(node)
                attrs['args'] = args
                attrs['tag_name'] = node.localName

                if node.nodeType == node.TEXT_NODE:
                    if not node.nodeValue.strip():
                        continue
                    attrs['value'] = node.nodeValue

                views.append(HtmlView(children=n, **attrs))


        return views

    def _make_field_widget(self, attrs, value=False):

        attrs['editable'] = self.editable
        if not attrs['type'] == 'many2one':
            attrs['link'] = self.link

        attrs.setdefault('context', self.context)
        attrs.setdefault('model', self.model)
        attrs.setdefault('state', self.state)

        if attrs.get('widget'):
            if attrs['widget']=='one2many_list':
                attrs['widget']='one2many'
            if get_widget(attrs['widget']):
                attrs['type2'] = attrs['type']
                attrs['type'] = attrs['widget']

        attrs['value'] = value

        name = attrs['name']
        kind = attrs.get('type', 'char')

        if kind == 'image' or kind == 'picture':
            attrs['id'] = self.id

        # suppress by container's readonly property
        if self.readonly:
            attrs['readonly'] = True

        field = get_widget(kind)(**attrs)

        if isinstance(field, TinyInputWidget):
            field.set_value(value)

        # update the record data
        cherrypy.request.terp_record[name] =  field.get_value()

        return field


# vim: ts=4 sts=4 sw=4 si et
