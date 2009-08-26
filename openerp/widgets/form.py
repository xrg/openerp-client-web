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

import os
import re
import time
import xml.dom.minidom

import cherrypy

from openerp import icons
from openerp import tools
from openerp import common
from openerp import cache

from openerp import rpc

from openerp.i18n import format
from openerp.i18n import get_locale
from openerp.utils import TinyDict

from interface import TinyInputWidget
from interface import ConcurrencyInfo

from base import JSLink, JSSource, CSSLink

from openerp import validators

class Frame(TinyInputWidget):
    """Frame widget layouts the widgets in a table.
    """

    template = "templates/frame.mako"

    params = ['table']
    member_widgets = ['hiddens', 'children']

    table = None

    def __init__(self, **attrs):

        super(Frame, self).__init__(**attrs)

        self.columns = int(attrs.get('col', 4))
        self.nolabel = True

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

            else:
                pass

        self.fields = []

        # properly distribute widths among columns

        if len(self.table) == 1:
            self.table[0] = [(a, w) for a, w in self.table[0] if getattr(w, 'visible', 1)]

        max_length = max([len(row) for row in self.table])

        for row in self.table:

            ## adjust the columns
            #if len(row):
            #    cs = reduce(lambda x,y: x +y, [a.get('colspan', 1) for a,w in row])
            #    a['colspan'] = a.get('colspan', 1) + self.columns - cs

            sn = len([w for a, w in row if isinstance(w, (basestring, Label))])
            pn = len([w for a, w in row if isinstance(w, Image)])

            sw = 5                                  # label width
            pw = 1                                  # image width
            ww = 100.00 - sw * sn - pw * pn         # remaining width
            cn = self.columns - sn - pn             # columns - (lables + image)

            cn -= len([w for a, w in row if not isinstance(w, (basestring, Label, Image)) and not w.visible])

            if cn < 1: cn = 1

            for i, (a, wid) in enumerate(row):

                if isinstance(wid, (basestring, Label)):
                    w = sw
                elif isinstance(wid, Image):
                    w = pw
                else:
                    c = a.get('colspan', 1)
                    if c > max_length:
                        c = 1

                    if wid.visible:
                        w = ww * c / cn
                    else:
                        w = 0

                a['width'] = '%d%%' % (w)

    def add_row(self):
        self.table.append([])

        self.x = 0
        self.y += 1

    def _add_validator(self, widget):

        if not isinstance(widget, TinyInputWidget) or \
                not widget.name or widget.readonly or \
                widget.name.startswith('_terp_listfields'):
            return

        if widget.validator:
            cherrypy.request.terp_validators[str(widget.name)] = widget.validator
            cherrypy.request.terp_fields += [widget]

    def add(self, widget, label=None, rowspan=1, colspan=1):

        if colspan > self.columns:
            colspan = self.columns

        a = label and 1 or 0

        if colspan + self.x + a > self.columns:
            self.add_row()

        if colspan == 1 and a == 1:
            colspan = 2

        tr = self.table[-1]

        if label:
            colspan -= 1
            attrs = {'class': 'label', 'title': getattr(widget, 'help', None), 'for': widget.name}
            td = [attrs, label]
            tr.append(td)

        if isinstance(widget, TinyInputWidget) and hasattr(cherrypy.request, 'terp_validators'):
            self._add_validator(widget)

        attrs = {'class': 'item', 'for': widget.name}
        if rowspan > 1: attrs['rowspan'] = rowspan
        if colspan > 1: attrs['colspan'] = colspan

        if not hasattr(widget, 'visible'):
            widget.visible = True

        # state change
        if getattr(widget, 'states', False):

            states = widget.states
            # convert into JS
            if isinstance(states, dict):
                states = states.copy()
                for k, v in states.items():
                    states[k] = dict(v)

            attrs['states'] = str(states)
            attrs['widget'] = widget.name
            if not widget.visible:
                attrs['style'] = 'display: none'
            widget.visible = True

        if isinstance(widget, (Group, Notebook, O2M, M2M)):
            attrs['valign'] = 'top'

        # attr change
        if getattr(widget, 'attributes', False):
            attrs['attrs'] = str(widget.attributes)
            attrs['widget'] = widget.name

        td = [attrs, widget]
        tr.append(td)

        self.x += colspan + a

    def add_hidden(self, widget):
        if isinstance(widget, TinyInputWidget) and hasattr(cherrypy.request, 'terp_validators'):
            self._add_validator(widget)
        self.hiddens += [widget]

class Notebook(TinyInputWidget):
    """Notebook widget, contains list of frames. Each frame will be displayed as a
    page of the the Notebook.
    """

    template = "templates/notebook.mako"

    javascript = [JSLink("openerp", "javascript/tabber/tabber_cookie.js"),
                  JSSource("""
                  if (typeof(tabberOptions) == "undefined")
                      var tabberOptions = {};
                  tabberOptions['onLoad'] = tabber_onload;
                  tabberOptions['onClick'] = tabber_onclick;
                  tabberOptions['cookie'] = 'TGTabber';
                  tabberOptions['manualStartup'] = true;"""),
                  JSLink("openerp", "javascript/tabber/tabber.js")]

    css = [CSSLink('openerp', 'css/tabs.css')]

    params = ['fake_widget']
    member_widgets = ['children']
    
    def __init__(self, **attrs):
        super(Notebook, self).__init__(**attrs)
        self.nolabel = True
        self.colspan = attrs.get('colspan', 3)
        
        self.fake_widget = '_fake'
        if attrs.get('prefix'):
            self.fake_widge = attrs['prefix'] + '/_fake'


class Page(Frame):
    def __init__(self, **attrs):
        super(Page, self).__init__(**attrs)
        if self.invisible:
            self.attributes = "{'invisible': [1]}"


class Separator(TinyInputWidget):
    """Separator widget.
    """

    template = "templates/separator.mako"
    params = ["position"]
    
    def __init__(self, **attrs):
        super(Separator, self).__init__(**attrs)

        self.colspan = int(attrs.get('colspan', 4))
        self.position = attrs.get('position', False)
        self.rowspan = 1
        self.nolabel = True


class NewLine(TinyInputWidget):
    """NewLine widget just tells the Frame widget to start new row during
    layout process.
    """
    template = "<span/>"


class Label(TinyInputWidget):

    template = """
    <div style="text-align: ${align}; width: 100%;">
        ${field_value}
    </div>"""

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

class Char(TinyInputWidget):

    template = "templates/char.mako"
    params = ['password', 'size']

    def __init__(self, **attrs):
        
        if attrs.get('password'):
            attrs.pop('invisible', None)
        
        super(Char, self).__init__(**attrs)
        self.validator = validators.String()

    def set_value(self, value):
        self.default = value


class Email(TinyInputWidget):
    template = "templates/email.mako"

    def __init__(self, **attrs):
        super(Email, self).__init__(**attrs)
        self.validator = validators.Email()

    def set_value(self, value):
        if value:
            self.default = value


class Text(TinyInputWidget):
    template = "templates/text.mako"

    def __init__(self, **attrs):
        super(Text, self).__init__(**attrs)
        self.validator = validators.String()

    def set_value(self, value):
        self.default = value


class Integer(TinyInputWidget):
    template = "templates/integer.mako"

    def __init__(self, **attrs):
        super(Integer, self).__init__(**attrs)
        self.validator = validators.Int()

    def set_value(self, value):
        self.default = value or 0


class Boolean(TinyInputWidget):
    template = "templates/boolean.mako"

    def __init__(self, **attrs):
        super(Boolean, self).__init__(**attrs)
        self.validator = validators.Bool()

    def set_value(self, value):
        self.default = value or ''


class Float(TinyInputWidget):
    template = "templates/float.mako"

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
        self.default = value


class FloatTime(TinyInputWidget):
    template = "templates/floattime.mako"

    def __init__(self, **attrs):
        super(FloatTime, self).__init__(**attrs)
        self.validator = validators.FloatTime()

    def set_value(self, value):
        self.default = value


class ProgressBar(TinyInputWidget):
    template = "templates/progressbar.mako"

    def __init__(self, **attrs):
        super(ProgressBar, self).__init__(**attrs)

        if attrs.get('type2') is 'float':
            self.validator = validators.Float()
        else:
            self.validator = validators.Int()

    def set_value(self, value):
        self.default = value or 0.00


class Selection(TinyInputWidget):
    template = "templates/selection.mako"

    params = ['options']
    options = []

    def __init__(self, **attrs):
        super(Selection, self).__init__(**attrs)

        # m2o as selection
        if attrs.get('relation') and attrs.get('widget') == 'selection':
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
                ctx.update(attrs.get('context', {}))
                self.options = proxy.name_get(ids, ctx)
            except:
                self.options = []
        else:
            self.options = attrs.get('selection', [])

        # determine the actual type
        if self.options and isinstance(self.options[0][0], basestring):
            self.kind = 'char'
            self.validator = validators.String()
        else:
            self.validator = validators.Selection()

    def set_value(self, value):

        if isinstance(value, (tuple, list)):
            value = value[0]

        if self.options and value not in dict(self.options):
            value = None

        super(Selection, self).set_value(value)

class DTLink(JSLink):
    
    def update_params(self, d):
        super(DTLink, self).update_params(d)
        
        lang = get_locale()
        link = "calendar/lang/calendar-%s.js" % lang
        
        if os.path.exists(tools.find_resource("openerp", "static", link)):
            d.link = tools.url(["/cp_widgets/openerp", link])
        else:
            lang = lang.split('_')[0]
            link = "calendar/lang/calendar-%s.js" % lang
            if os.path.exists(tools.find_resource("openerp", "static", link)):
                d.link = tools.url(["/cp_widgets/openerp", link])

class DateTime(TinyInputWidget):

    template = "templates/datetime.mako"
    
    javascript = [JSLink("openerp", "calendar/calendar.js"),
                  JSLink("openerp", "calendar/calendar-setup.js"),
                  DTLink("openerp", "calendar/lang/calendar-en.js")]
                            
    css = [CSSLink("openerp", "calendar/skins/aqua/theme.css")]

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


class URL(TinyInputWidget):
    template = "templates/url.mako"

    def __init__(self, **attrs):
        super(URL, self).__init__(**attrs)
        self.validator = validators.URL()

    def set_value(self, value):
        if value:
            super(URL, self).set_value(value)

class Hidden(TinyInputWidget):
    template = "templates/hidden.mako"

    params = ['relation', 'field_id']
    member_widgets = ['widget']

    def __init__(self, **attrs):
        super(Hidden, self).__init__(**attrs)
        kind = self.kind or 'text'
        self.widget = WIDGETS[kind](**attrs)
        self.validator = self.widget.validator
        self.relation = attrs.get('relation') or None
        
        if 'field_id' not in attrs:
            self.field_id = self.name
            
    def set_value(self, value):
        self.widget.set_value(value)
        self.default = self.widget.default

class Button(TinyInputWidget):

    template = "templates/button.mako"
    params = ["btype", "id", "confirm", "icon", "target"]

    visible = True
    target = 'current'

    def __init__(self, **attrs):

        super(Button, self).__init__(**attrs)

        # remove mnemonic
        self.string = re.sub('_(?!_)', '', self.string or '')

        self.btype = attrs.get('special', attrs.get('type', 'workflow'))

        self.nolabel = True
        self.readonly = False

        if self.icon:
            self.icon = icons.get_icon(self.icon)

    def set_state(self, state):
        if self.states:
            self.visible = state in self.states

        
class Group(TinyInputWidget):
    template = "templates/group.mako"

    member_widgets = ["frame"]

    def __init__(self, **attrs):
        super(Group, self).__init__(**attrs)

        self.frame = Frame(**attrs)
        self.nolabel = True


class Dashbar(TinyInputWidget):

    template = "templates/dashbar.mako"

    javascript = [JSLink("openerp", "javascript/dashboard.js")]
    css = [CSSLink('openerp', 'css/dashboard.css')]

    member_widgets = ['children']


class HPaned(TinyInputWidget):

    template = """
    <table width="100%" class="hpaned">
        <tr>
            % for child in children:
            <td valign="top">
                ${display_member(child)}
            </td>
            % endfor
        </tr>
    </table>
    """
    
    member_widgets = ['children']

    def __init__(self, **attrs):
        super(HPaned, self).__init__(**attrs)
        self.nolabel = True


class VPaned(TinyInputWidget):

    template = """
    <table width="100%" class="vpaned">
        % for child in children:
        <tr>
            <td valign="top">
                ${display_member(child)}
            </td>
        </tr>
        % endfor
    </table>
    """
    
    member_widgets = ['children']

    def __init__(self, **attrs):
        super(VPaned, self).__init__(**attrs)
        self.nolabel = True


class Form(TinyInputWidget):
    """A generic form widget
    """

    template = """
    % if frame:
        ${concurrency_info.display()}
        ${display_member(frame)}
    % endif
    """

    params = ['id']
    member_widgets = ['frame', 'concurrency_info']

    def __init__(self, prefix, model, view, ids=[], domain=[], context={}, editable=True, readonly=False, nodefault=False, nolinks=1):

        super(Form, self).__init__(prefix=prefix, model=model, editable=editable, readonly=readonly, nodefault=nodefault)

        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]
        attrs = tools.node_attributes(root)
        fields = view['fields']

        self.string = attrs.get('string', '')
        self.link = attrs.get('link', nolinks)

        self.id = None
        self.context = context or {}

        proxy = rpc.RPCProxy(model)

        ctx = rpc.session.context.copy()
        ctx.update(context)
        ctx['bin_size'] = True

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
            values = proxy.read(ids[:1], fields.keys() + ['__last_update'], ctx)[0]
            self.id = ids[0]
            self._update_concurrency_info(self.model, [values])

        elif 'datas' in view: # wizard data

            for f in fields:
                if 'value' in fields[f]:
                    values[f] = fields[f]['value']

            values.update(view['datas'])

        elif not self.nodefault: # default
            defaults = proxy.default_get(fields.keys(), ctx)

        elif 'state' in fields: # if nodefault and state get state only
            defaults = proxy.default_get(['state'], ctx)

        elif 'x_state' in fields: # if nodefault and x_state get x_state only (for custom objects)
            defaults = proxy.default_get(['x_state'], ctx)

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
                if kind not in WIDGETS:
                    continue

                attrs['prefix'] = prefix
                attrs['name'] = name
                attrs['readonly'] = True # always make them readonly

                field = self._make_field_widget(attrs, values.get(name))
                self.frame.add_hidden(field)

    def parse(self, prefix='', root=None, fields=None, values={}):

        views = []

        for node in root.childNodes:

            if not node.nodeType==node.ELEMENT_NODE:
                continue

            attrs = tools.node_attributes(node)
            attrs['prefix'] = prefix
            attrs['state'] = self.state

            if node.localName=='image':
                views += [Image(**attrs)]

            elif node.localName=='separator':
                views += [Separator(**attrs)]

            elif node.localName=='label':
                text = attrs.get('string', '')
                
                if not text:
                    for node in node.childNodes:
                        if node.nodeType == node.TEXT_NODE:
                            text += node.data
                        else:
                            text += node.toxml()
                            
                attrs['string'] = text
                views += [Label(**attrs)]

            elif node.localName=='newline':
                views += [NewLine(**attrs)]

            elif node.localName=='button':
                views += [Button(model=self.model, id=self.id, **attrs)]

            elif node.localName == 'form':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views += [Frame(children=n, **attrs)]

            elif node.localName == 'notebook':
                self.nb_couter += 1
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                nb = Notebook(children=n, **attrs)
                nb._name = prefix.replace('/', '_') + '_notebook_%s'  % (self.nb_couter)
                views += [nb]

            elif node.localName == 'page':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views += [Page(children=n, **attrs)]

            elif node.localName=='group':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views += [Group(children=n, **attrs)]

            elif node.localName == 'field':
                name = attrs['name']

                try:
                    fields[name].update(attrs)
                except:
                    print "-"*30,"\n malformed tag for:", attrs
                    print "-"*30
                    raise

                kind = fields[name]['type']

                if kind not in WIDGETS:
                    continue

                if kind in ('text', 'text_tag') and attrs.get('html'):
                    kind = 'text_html'

                if name in self.view_fields:
                    print "-"*30
                    print " malformed view for:", self.model
                    print " duplicate field:", name
                    print "-"*30
                    raise common.error(_('Application Error!'), _('Invalid view, duplicate field: %s') % name)

                self.view_fields.append(name)

                field = self._make_field_widget(fields[name], values.get(name))
                views += [field]

            elif node.localName=='hpaned':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views += [HPaned(children=n, **attrs)]

            elif node.localName=='vpaned':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views += [VPaned(children=n, **attrs)]

            elif node.localName in ('child1', 'child2'):
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                attrs['name'] = tools.get_node_xpath(node)
                views += [Dashbar(children=n, **attrs)]

            elif node.localName=='action':
                views += [Action(**attrs)]
                cherrypy.request._terp_dashboard = True

        return views

    def _make_field_widget(self, attrs, value=False):

        attrs['editable'] = self.editable
        attrs['link'] = self.link

        attrs.setdefault('context', self.context)
        attrs.setdefault('model', self.model)
        attrs.setdefault('state', self.state)

        if attrs.get('widget', False):
            if attrs['widget']=='one2many_list':
                attrs['widget']='one2many'
            if attrs['widget'] in WIDGETS:
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

        field = WIDGETS[kind](**attrs)

        if isinstance(field, TinyInputWidget):
            field.set_value(value)

        # update the record data
        cherrypy.request.terp_record[name] =  field.get_value()

        return field


from action import Action
from many2one import M2O
from one2many import O2M
from many2many import M2M
from reference import Reference
from tiny_mce import TinyMCE
from wiki import WikiWidget
from binary import Binary
from binary import Image
from binary import Picture

WIDGETS = {
    'date': DateTime,
    'time': DateTime,
    'float_time': FloatTime,
    'datetime': DateTime,
    'float': Float,
    'integer': Integer,
    'selection': Selection,
    'char': Char,
    'boolean': Boolean,
    'button': Button,
    'reference': Reference,
    'binary': Binary,
    'picture': Picture,
    'text': Text,
    'text_tag': Text,
    'text_html': TinyMCE,
    'text_wiki': WikiWidget,
    'one2many': O2M,
    'one2many_form': O2M,
    'one2many_list': O2M,
    'many2many': M2M,
    'many2one': M2O,
    'email' : Email,
    'url' : URL,
    'image' : Image,
    'progressbar' : ProgressBar,
}

# vim: ts=4 sts=4 sw=4 si et

