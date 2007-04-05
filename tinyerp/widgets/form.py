###############################################################################
#
# Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id$
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

"""
This module implementes widget parser for form view, and
several widget components.
"""

import xml.dom.minidom

import turbogears as tg
import cherrypy

from tinyerp import tools
from tinyerp import rpc

from interface import TinyField
from interface import TinyWidget
from interface import TinyInputWidget
from interface import TinyCompoundWidget

import validators as tiny_validators

class Frame(TinyCompoundWidget):
    """Frame widget layouts the widgets in a table.

    @todo: only render fields during self.display
    @todo: use value_for, param_for with field.display
    """

    template = "tinyerp.widgets.templates.frame"

    params = ['table']
    member_widgets = ['children']

    table = []

    def __init__(self, attrs, children, columns=4):
        """Create new instance of Frame widget."

        @param attrs: attributes
        @param children: child widgets
        @param columns: number of layout columns

        @return: an instance of Frame widget
        """

        super(Frame, self).__init__(attrs)

        self.columns = columns
        self.nolabel = True

        self.add_row()

        self.children = children

        for child in children:

            string = not child.nolabel and child.string
            rowspan = child.rowspan or 1
            colspan = child.colspan or 1

            self.add2(child, string, rowspan=rowspan, colspan=colspan)

        self.fields = []

    def add_row(self):
        self.table.append([])
        self.cols = self.columns

    def new_line(self):
        self.add_row()

    def add(self, widget, rowspan=1, colspan=1, css_class=None):

        if self.cols == 0:
            self.add_row()

        if isinstance(widget, TinyWidget) and widget.colspan == self.columns and self.cols < self.columns and widget.nolabel == False:
            colspan = self.columns - 1

        if self.cols < colspan:
            self.add_row()

        tr = self.table[-1]

        attrs = {}
        if rowspan > 1: attrs['rowspan'] = rowspan
        if colspan > 1: attrs['colspan'] = colspan
        if css_class: attrs['class'] = css_class

        td = [attrs]

        if isinstance(widget, TinyInputWidget) and hasattr(cherrypy.request, 'terp_validators') and widget.name and widget.validator:
            cherrypy.request.terp_validators[str(widget.name)] = widget.validator
            cherrypy.request.terp_fields += [widget]

        td.append(widget)
        tr.append(td)

        self.cols -= colspan

    def add2(self, item, label=None, rowspan=1, colspan=1):
        if not item: return

        if isinstance(item, NewLine):
            self.new_line()
            return

        if label:
            if self.cols < colspan:
                self.add_row()

            self.add(label, css_class='label')

        self.add(item, rowspan=rowspan, colspan=colspan, css_class='item')

    def display(self, value=None, **params):
        return super(Frame, self).display(value, **params)

class Notebook(TinyCompoundWidget):
    """Notebook widget, contains list of frames. Each frame will be displayed as a
    page of the the Notebook.
    """

    template = """
    <div class='tabber' xmlns:py="http://purl.org/kid/ns#">
        <div class='tabbertab' py:for="page in children">
            <h3>${page.string}</h3>
            <div>
                ${page.display(value_for(page), **params_for(page))}
            </div>
        </div>
    </div>
    """

    member_widgets = ['_notebook_', "children"]
    _notebook_ = tg.widgets.Tabber()

    def __init__(self, attrs, children):
        super(Notebook, self).__init__(attrs)

        self.children = children
        self.nolabel = True

class Separator(TinyField):
    """Separator widget.
    """

    params = ['string']
    template = "tinyerp.widgets.templates.separator"

    def __init__(self, attrs={}):
        super(Separator, self).__init__(attrs)

        self.colspan = 4
        self.rowspan = 1
        self.nolabel = True

class NewLine(TinyField):
    """NewLine widget just tells the Frame widget to start new row during
    layout process.
    """
    template = "<span/>"

class Label(TinyField):
    template = """<div style="text-align: center; width: 100%" xmlns:py="http://purl.org/kid/ns#">
        ${field_value}
    </div>
    """
    params = ["field_value"]

    def __init__(self, attrs={}):
        super(Label, self).__init__(attrs)

        self.nolabel = True
        self.field_value = self.string

    def set_value(self, value):
        self.field_value = unicode(value or '', 'utf-8')

class Char(TinyField):
    template = "tinyerp.widgets.templates.char"

    def __init__(self, attrs={}):
        super(Char, self).__init__(attrs)

    def set_value(self, value):
        self.default = unicode(value or '', 'utf-8')

class Text(TinyField):
    template = "tinyerp.widgets.templates.text"

    def __init__(self, attrs={}):
        super(Text, self).__init__(attrs)

    def set_value(self, value):
        self.default = unicode(value or '', 'utf-8')

class Integer(TinyField):
    template = "tinyerp.widgets.templates.integer"

    def __init__(self, attrs={}):
        super(Integer, self).__init__(attrs)
        self.validator = tiny_validators.Int()

    def set_value(self, value):
        if value:
            self.default = int(value)

class Boolean(TinyField):
    template = "tinyerp.widgets.templates.boolean"
    params = ["checked"]
    checked = {}

    def __init__(self, attrs={}):
        super(Boolean, self).__init__(attrs)
        self.validator = tiny_validators.Bool()

    def set_value(self, value):
        self.default = value or ''

        if value:
            self.checked['checked'] = "1"

class Float(TinyField):
    template = "tinyerp.widgets.templates.float"

    def __init__(self, attrs={}):
        super(Float, self).__init__(attrs)
        self.validator = tiny_validators.Float()

    def set_value(self, value):
        self.default = value

class Selection(TinyField):
    template = "tinyerp.widgets.templates.selection"
    params = ['options']
    options = []

    def __init__(self, attrs={}):
        super(Selection, self).__init__(attrs)
        self.options = attrs.get('selection', [])
        self.validator = tiny_validators.Selection()

class DateTime(TinyInputWidget, tg.widgets.CalendarDatePicker):
    template = "tinyerp.widgets.templates.datetime"
    params = ["format"]
    format = "%Y-%m-%d %H:%M"
    picker_shows_time = True
    button_text = 'Select'

    def __init__(self, attrs={}):
        TinyInputWidget.__init__(self, attrs)
        tg.widgets.CalendarDatePicker.__init__(self, name=self.name, not_empty=False)

        if attrs['type'] == 'date':
            self.format = "%Y-%m-%d"
            self.picker_shows_time = False
        elif attrs['type'] == 'time':
            self.format = "%H:%M"

        self.validator = tiny_validators.DateTime(format=self.format)

    def set_value(self, value):
        self._default = value

class Button(TinyField):
    """Button widget

    @todo: use states
    @todo: actions
    """

    template = """<button type="button" style="width: 100%" id="${name}" name="${name}">${string}</button>"""
    params = ["name", "string"]

    def __init__(self, attrs={}):
        TinyField.__init__(self, attrs)

        self.nolabel = True

class Group(TinyCompoundWidget):
    template = """
    <span xmlns:py="http://purl.org/kid/ns#">
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

        self.frame = Frame(attrs, children, columns=int(attrs.get('col', 4)))
        self.nolabel = True

class Form(TinyCompoundWidget):
    """A generic form widget
    """

    template = """
    <span xmlns:py="http://purl.org/kid/ns#" py:if="frame">
        ${frame.display(value_for(frame), **params_for(frame))}
    </span>
    """

    member_widgets = ['frame']
    frame = None

    def __init__(self, prefix, model, view, ids=[], domain=[], context={}, selectable=False, editable=False):

        super(Form, self).__init__()

        fields = view['fields']

        dom = xml.dom.minidom.parseString(view['arch'])
        root = dom.childNodes[0]
        attrs = tools.node_attributes(root)
        self.string = attrs.get('string', '')

        proxy = rpc.RPCProxy(model)

        values = {}
        if ids:
            values = proxy.read(ids[:1], fields.keys(), context)[0]
        else: #default
            values = proxy.default_get(fields.keys(), context)

        self.frame = self.parse(prefix, dom, fields, values)[0]

    def parse(self, prefix='', root=None, fields=None, values={}):

        views = []

        for node in root.childNodes:

            if not node.nodeType==node.ELEMENT_NODE:
                continue

            attrs = tools.node_attributes(node)
            attrs['prefix'] = prefix

            if node.localName=='image':
                pass

            elif node.localName=='separator':
                views += [Separator(attrs)]

            elif node.localName=='label':
                views += [Label(attrs)]

            elif node.localName=='newline':
                views += [NewLine(attrs)]

            elif node.localName=='button':
                views += [Button(attrs)]

            elif node.localName == 'form':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views += [Frame(attrs, n)]

            elif node.localName == 'notebook':
                n = self.parse(prefix=prefix, root=node, fields=fields, values=values)
                views += [Notebook(attrs, n)]

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

                try:
                    fields[name].update(attrs)
                except:
                    print "-"*30,"\n malformed tag for :", attrs
                    print "-"*30
                    raise

                kind = fields[name]['type']

                if kind not in widgets_type:
                    continue

                field = widgets_type[kind](attrs=fields[name])

                if values.has_key(name) and isinstance(field, TinyInputWidget):
                    field.set_value(values[name])

                views += [field]

        return views

from many2one import M2O
from one2many import O2M
from many2many import M2M

widgets_type = {
    'date': DateTime,
    'time': DateTime,
    'datetime': DateTime,
    'float': Float,
    'integer': Integer,
    'selection': Selection,
    'char': Char,
    'boolean': Boolean,
    'button': Button,
    #'reference': Reference,
    #'binary': Binary,
    #'picture': Picture,
    'text': Text,
    #'text_tag': TextTag,
    'one2many': O2M,
    #'one2many_form': O2M,
    #'one2many_list': O2M,
    'many2many': M2M,
    'many2one': M2O,
    'email' : Char,
    'url' : Char,
    #'image' : Image,
}
