###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id$
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

import time
import xml.dom.minidom

import turbogears as tg
import cherrypy

from tinyerp import icons
from tinyerp import tools
from tinyerp import format
from tinyerp import rpc

from tinyerp.utils import TinyDict

from interface import TinyField
from interface import TinyInputWidget
from interface import TinyCompoundWidget

import validators as tiny_validators

class Frame(TinyCompoundWidget):
    """Frame widget layouts the widgets in a table.
    """

    template = "tinyerp.widgets.templates.frame"

    params = ['table']
    member_widgets = ['children', 'hiddens']

    hiddens = None
    table = []

    def __init__(self, attrs, children):
        """Create new instance of Frame widget."

        @param attrs: attributes
        @param children: child widgets

        @return: an instance of Frame widget
        """

        super(Frame, self).__init__(attrs)

        self.columns = int(attrs.get('col', 4))
        self.nolabel = True

        self.x = 0
        self.y = 0

        self.add_row()

        self.children = children
        self.hiddens = []

        for child in children:

            string = not child.nolabel and child.string
            rowspan = child.rowspan or 1
            colspan = child.colspan or 1

            if isinstance(child, NewLine):
                self.add_row()
            elif getattr(child, 'visible', True) or isinstance(child, Button):
                self.add(child, string, rowspan, colspan)
            elif isinstance(child, TinyInputWidget):
                self.hiddens += [child]
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
            attrs = {'class': 'label'}
            td = [attrs, label]
            tr.append(td)

        if isinstance(widget, TinyInputWidget) and hasattr(cherrypy.request, 'terp_validators') and widget.name and widget.validator and not widget.readonly:
            cherrypy.request.terp_validators[str(widget.name)] = widget.validator
            cherrypy.request.terp_fields += [widget]

        attrs = {'class': 'item'}
        if rowspan > 1: attrs['rowspan'] = rowspan
        if colspan > 1: attrs['colspan'] = colspan

        if not hasattr(widget, 'visible'):
            widget.visible = True
            
        if isinstance(widget, (Group, Notebook, O2M, M2M)):
            attrs['valign'] = 'top'

        td = [attrs, widget]
        tr.append(td)

        self.x += colspan + a

class Notebook(TinyCompoundWidget):
    """Notebook widget, contains list of frames. Each frame will be displayed as a
    page of the the Notebook.
    """

    template = "tinyerp.widgets.templates.notebook"

    member_widgets = ['_notebook_', "children"]
    _notebook_ = tg.widgets.Tabber(use_cookie=True)
    _notebook_.css = [tg.widgets.CSSLink('tinyerp', 'css/tabs.css')]

    def __init__(self, attrs, children):
        super(Notebook, self).__init__(attrs)
        self.children = children
        self.nolabel = True

        self.colspan = attrs.get('colspan', 3)

class Separator(TinyField):
    """Separator widget.
    """

    params = ['string']
    template = "tinyerp.widgets.templates.separator"

    def __init__(self, attrs={}):
        super(Separator, self).__init__(attrs)

#        self.colspan = 4
        self.rowspan = 1
        self.nolabel = True

class NewLine(TinyField):
    """NewLine widget just tells the Frame widget to start new row during
    layout process.
    """
    template = """ <span/> """

class Label(TinyField):

    template = """
        <div style="text-align: center; width: 100%" xmlns:py="http://purl.org/kid/ns#">
            ${field_value}
        </div>   """

    params = ["field_value"]

    def __init__(self, attrs={}):
        super(Label, self).__init__(attrs)

        self.nolabel = True
        self.field_value = self.string

    def set_value(self, value):
        self.field_value = unicode(value or '', 'utf-8')

class Char(TinyField):
    template = "tinyerp.widgets.templates.char"
    params = ['password', 'size']
    invisible = False

    def __init__(self, attrs={}):
        super(Char, self).__init__(attrs)
        self.validator = tiny_validators.String()
        self.password = attrs.get('password', False)
        self.size = attrs.get('size')

    def set_value(self, value):
        self.default = value

class Email(TinyField):
    template = "tinyerp.widgets.templates.email"

    def __init__(self, attrs={}):
        super(Email, self).__init__(attrs)
        self.validator = tiny_validators.Email()

    def set_value(self, value):
        if value:
            self.default = value

class Text(TinyField):
    template = "tinyerp.widgets.templates.text"
    params = ['inline']
    javascript = [tg.widgets.JSLink("tinyerp", "javascript/textarea.js")]
    
    inline = False

    def __init__(self, attrs={}):
        super(Text, self).__init__(attrs)
        self.inline = attrs.get('inline', 0)
        self.validator = tiny_validators.String()

    def set_value(self, value):
        self.default = value

class Integer(TinyField):
    template = "tinyerp.widgets.templates.integer"

    def __init__(self, attrs={}):
        super(Integer, self).__init__(attrs)
        self.validator = tiny_validators.Int()

#        if not self.default:
#            self.default = 0

    def set_value(self, value):
        if value:
            self.default = int(value)

class Boolean(TinyField):
    template = "tinyerp.widgets.templates.boolean"

    def __init__(self, attrs={}):
        super(Boolean, self).__init__(attrs)
        self.validator = tiny_validators.Bool()

    def set_value(self, value):
        self.default = value or ''

class Float(TinyField):
    template = "tinyerp.widgets.templates.float"

    def __init__(self, attrs={}):
        super(Float, self).__init__(attrs)

        digits = attrs.get('digits', (16,2))
        if isinstance(digits, basestring):
            digits = eval(digits)

        integer, digit = digits

        self.validator = tiny_validators.Float(digit=digit)

#        if not self.default:
#            self.default = 0.0

    def set_value(self, value):
        self.default = value

class FloatTime(TinyField):
    template = "tinyerp.widgets.templates.floattime"

    def __init__(self, attrs={}):
        super(FloatTime, self).__init__(attrs)
        self.validator = tiny_validators.FloatTime()

    def set_value(self, value):
        self.default = value

class Selection(TinyField):
    template = "tinyerp.widgets.templates.selection"

    params = ['options']
    options = []

    def __init__(self, attrs={}):
        super(Selection, self).__init__(attrs)
        self.options = attrs.get('selection', [])

        # determine the actual type
        if self.options and isinstance(self.options[0][0], basestring):
            self.kind = 'char'
            self.validator = tiny_validators.String()
        else:
            self.validator = tiny_validators.Selection()

    def set_value(self, value):
        super(Selection, self).set_value(value)

class DateTime(TinyInputWidget, tg.widgets.CalendarDatePicker):
    template = "tinyerp.widgets.templates.datetime"

    params = ["format"]

    format = '%Y-%m-%d %H:%M:%S'
    picker_shows_time = True
    button_text = 'Select'
    
    css = [tg.widgets.CSSLink(tg.widgets.base.static, "calendar/skins/aqua/theme.css")]

    def __init__(self, attrs={}):
        TinyInputWidget.__init__(self, attrs)
        tg.widgets.CalendarDatePicker.__init__(self, name=self.name, not_empty=False)
        
        self.format = format.get_datetime_format(attrs['type'])

        if attrs['type'] == 'date':
            self.picker_shows_time = False

        self.validator = tiny_validators.DateTime(kind=attrs['type'])

    def set_value(self, value):
        self._default = value or False

class Binary(TinyField):
    template = "tinyerp.widgets.templates.binary"
    params = ["name", "text", "readonly"]

    text = None
    file_upload = True

    def __init__(self, attrs={}):
        super(Binary, self).__init__(attrs)
        self.validator = tiny_validators.Binary()

    def set_value(self, value):
        if value:
            #super(Binary, self).set_value("%s bytes" % len(value))
            self.text = "%s bytes" % len(value)

class Url(TinyField):
    template = "tinyerp.widgets.templates.url"

    def __init__(self, attrs={}):
        super(Url, self).__init__(attrs)
        self.validator = tiny_validators.Url()

    def set_value(self, value):
        if value:
            super(Url, self).set_value(value)

class Hidden(TinyField):
    template = "tinyerp.widgets.templates.hidden"
    wid = None

    def __init__(self, attrs={}):
        super(Hidden, self).__init__(attrs)
        self.wid = widgets_type[self.kind](attrs)
        self.validator = self.wid.validator

    def set_value(self, value):
        self.wid.set_value(value)
        self.default = self.wid.default

class Button(TinyField):
    """Button widget

    @todo: use states
    @todo: actions
    """

    template = "tinyerp.widgets.templates.button"
    params = ["name", "string", "model", "btype", "id", "confirm", "icon"]

    visible = True

    def __init__(self, current_model, id=None, attrs={}):

        TinyField.__init__(self, attrs)

        self.btype = attrs.get('type', 'workflow')
        self.confirm = attrs.get('confirm', None)

        self.model = current_model
        self.id = id

        self.nolabel = True
        if 'icon' in attrs:
            self.icon = icons.get_icon(attrs['icon'])

    def set_state(self, state):
        if self.states:
            self.visible = state in self.states

class Image(TinyField):

    template = """
        <span xmlns:py="http://purl.org/kid/ns#" py:strip="">
            <img py:if="stock" align="left" src="${src}" width="${width}" height="${height}"/>
            <img py:if="not stock and id and editable" id="${field}" border='1' alt="Click here to add new image." align="left" src="${src}" width="${width}" height="${height}" onclick="openWindow(getURL('/image', {model: '${model}', id: ${id}, field : '${field}'}), {width: 500, height: 300});"/>
            <img py:if="not stock and id and not editable" id="${field}" border='1' align="left" src="${src}" width="${width}" height="${height}"/>
        </span>
        """

    params = ["src", "width", "height", "model", "id", "field", "stock"]
    src = ""
    width = 32
    height = 32
    id = None
    field = ''
    stock = True

    def __init__(self, attrs={}):
        icon = attrs.get('name')
        attrs['name'] = attrs.get('name', 'Image').replace("-","_")

        TinyField.__init__(self, attrs)

        if 'widget' in attrs:
            self.stock = False
            self.src = '/image/get_image?model=%s&id=%s&field=%s' % (attrs['model'], attrs['id'], self.name)
            self.height = attrs.get('img_height', 160)
            self.width = attrs.get('img_width', 200)
            self.id = attrs['id']
            self.field = self.name
        else:
            self.src =  icons.get_icon(icon)

class Group(TinyCompoundWidget):
    template = """
    <span xmlns:py="http://purl.org/kid/ns#" py:strip="">
        <fieldset py:if="string">
            <legend py:content="string" />
            ${frame.display(value_for(frame), **params_for(frame))}
        </fieldset>
        <span py:replace="frame.display()" py:if="not string"/>
    </span>
    """

    params = ["string"]
    member_widgets = ["frame"]
    frame = None

    def __init__(self, attrs, children):
        TinyCompoundWidget.__init__(self, attrs)

        self.frame = Frame(attrs, children)
        self.nolabel = True

class HPaned(TinyCompoundWidget):

    template = """
        <span xmlns:py="http://purl.org/kid/ns#" py:strip="">
            <table width="100%" class="hpaned">
                <tr>
                    <td valign="top" py:for="child in children" py:content="child.display(value_for(child), **params_for(child))"></td>
                </tr>
            </table>
        </span>
        """

    member_widgets = ["children"]

    def __init__(self, attrs, children):
        super(HPaned, self).__init__(attrs)
        self.children = children
        self.nolabel = True

class VPaned(TinyCompoundWidget):

    template = """
        <span xmlns:py="http://purl.org/kid/ns#" py:strip="">
            <table width="100%" class="hpaned">
                <tr py:for="child in children">
                    <td valign="top" py:content="child.display(value_for(child), **params_for(child))"></td>
                </tr>
            </table>
        </span>
        """

    member_widgets = ["children"]

    def __init__(self, attrs, children):
        super(VPaned, self).__init__(attrs)
        self.children = children
        self.nolabel = True

class Form(TinyCompoundWidget):
    """A generic form widget
    """

    template = """
        <span xmlns:py="http://purl.org/kid/ns#" py:if="frame" py:replace="frame.display(value_for(frame), **params_for(frame))"/>
        """

    member_widgets = ['frame']
    frame = None

    def __init__(self, prefix, model, view, ids=[], domain=[], context={}, editable=True, readonly=False, nodefault=False, nolinks=1):
        super(Form, self).__init__()

        fields = view['fields']
        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]
        attrs = tools.node_attributes(root)
        self.string = attrs.get('string', '')

        self.link = attrs.get('link', nolinks)

        self.model = model
        self.id = None
        self.editable = editable
        self.readonly = readonly

        proxy = rpc.RPCProxy(model)

        ctx = rpc.session.context.copy()
        ctx.update(context)

        values = {}
        defaults = {}

        # update values according to domain
        for d in domain:
            if d[1] == '=':
                values[d[0]] = d[2]

        if ids:
            values = proxy.read(ids[:1], fields.keys(), ctx)[0]
            self.id = ids[0]

        elif 'datas' in view: # wizard data

            for f in fields:
                if 'value' in fields[f]:
                    values[f] = fields[f]['value']

            values.update(view['datas'])

        elif not nodefault: # default
            defaults = proxy.default_get(fields.keys(), ctx)

        elif 'state' in fields: # if nodefault and state get state only
            defaults = proxy.default_get(['state'], ctx)

        for k, v in defaults.items():
            values.setdefault(k, v)

        # store current record values in request object (see, self.parse & O2M default_get_ctx) 
        cherrypy.request.terp_record = TinyDict()

        self.frame = self.parse(prefix, dom, fields, values)[0]

    def parse(self, prefix='', root=None, fields=None, values={}):

        views = []

        for node in root.childNodes:

            if not node.nodeType==node.ELEMENT_NODE:
                continue

            attrs = tools.node_attributes(node)

            attrs['prefix'] = prefix
            attrs['editable'] = self.editable
            
            attrs['link'] = self.link

            if 'state' in values:
                attrs['state'] = values['state']

            attrs['model'] = attrs.get('model', self.model)
            #attrs['readonly'] = attrs.get('readonly', self.readonly)   #(For testing Binary widget remove coment...)

            if node.localName=='image':
                views += [Image(attrs)]

            elif node.localName=='separator':
                views += [Separator(attrs)]

            elif node.localName=='label':
                views += [Label(attrs)]

            elif node.localName=='newline':
                views += [NewLine(attrs)]

            elif node.localName=='button':
                views += [Button(self.model, self.id, attrs)]

            elif node.localName == 'form':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views += [Frame(attrs, n)]

            elif node.localName == 'notebook':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                nb = Notebook(attrs, n)
                nb.name = prefix.replace('/', '_') + '_notebook'
                views += [nb]

            elif node.localName == 'page':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views += [Frame(attrs, n)]

            elif node.localName=='group':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views += [Group(attrs, n)]

            elif node.localName == 'field':
                name = attrs['name']

                if attrs.get('widget', False):
                    if attrs['widget']=='one2many_list':
                        attrs['widget']='one2many'
                    attrs['type'] = attrs['widget']

                # XXX: update widgets also
                attrs['value'] = values.get(name, None)

                # password field? then let XML attrs overrides invisible property.
                if fields[name].get('type') == 'char' and 'invisible' in fields[name]:
                    attrs['password'] = fields[name].pop('invisible')

                try:
                    fields[name].update(attrs)
                except:
                    print "-"*30,"\n malformed tag for :", attrs
                    print "-"*30
                    raise
                
                # suppress by container's readonly property 
                if self.readonly:
                    attrs['readonly'] = True
                
                kind = fields[name]['type']

                if kind not in widgets_type:
                    continue
                
                if kind in ('text', 'text_tag') and attrs.get('html'):
                    try:
                        cherrypy.request.headers["User-Agent"].index('Safari')
                    except:
                        kind = 'html_tag'

                if kind == 'image':
                    fields[name]['id'] = self.id

                field = widgets_type[kind](attrs=fields[name])

                if values.has_key(name) and isinstance(field, TinyInputWidget):
                    field.set_value(values[name])
                
                # update the record data
                cherrypy.request.terp_record[field.name] =  field.get_value()

                views += [field]

            elif node.localName=='hpaned':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views += [HPaned(attrs, n)]

            elif node.localName=='vpaned':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views += [VPaned(attrs, n)]

            elif node.localName in ('child1', 'child2'):
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views += [Frame(attrs, n)]

            elif node.localName=='action':
                views += [Action(attrs)]

        return views

from action import Action
from many2one import M2O
from one2many import O2M
from many2many import M2M
from reference import Reference
from tiny_mce import TinyMCE

widgets_type = {
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
    #'picture': Picture,
    'text': Text,
    'text_tag': Text,
    'html_tag': TinyMCE,
    'one2many': O2M,
    'one2many_form': O2M,
    'one2many_list': O2M,
    'many2many': M2M,
    'many2one': M2O,
    'email' : Email,
    'url' : Url,
    'image' : Image
}
