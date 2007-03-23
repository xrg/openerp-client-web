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
from elementtree import ElementTree as ET

import turbogears as tg

from tinyerp import tools
from tinyerp import rpc

class TinyWidget(object):
    """Widget interface, every widget class should implement
    this class.
    """

    colspan = 1
    rowspan = 1
    string = None
    nolabel = False
    select = False

    def __init__(self, attrs={}):

        self.string = attrs.get("string", None)
        self.model = attrs.get("model", None)

        self.name = attrs['prefix'] + (attrs['prefix'] and '/' or '') + attrs.get('name', '')

        self.colspan = int(attrs.get('colspan', 1))
        self.rowspan = int(attrs.get('rowspan', 1))
        self.select = int(attrs.get('select', 0))
        self.nolabel = int(attrs.get('nolabel', 0))

class TinyField(TinyWidget):
    """Interface for Field widgets, every InputField widget should
    implement this class
    """

    field_value = None

    def get_value(self):
        """Get the value of the field.

        @return: field value
        """
        return self.field_value

    def set_value(self, value):
        """Set the value of the field.

        @param value: the value
        """
        self.field_value = value

class Frame(tg.widgets.CompoundWidget, TinyWidget):
    """Frame widget layouts the widgets in a table.
    """

    template = """
    <div xmlns:py="http://purl.org/kid/ns#" py:replace="table"/>
    """

    params = ['table']
    member_widgets = ['children']

    def __init__(self, attrs, children, columns=4):
        """Create new instance of Frame widget."

        @param attrs: attributes
        @param children: child widgets
        @param columns: number of layout columns

        @return: an instance of Frame widget
        """

        TinyWidget.__init__(self, attrs)
        tg.widgets.CompoundWidget.__init__(self, name="Frame")

        self.columns = columns
        self.nolabel = True

        self.table = ET.Element('table', width="100%")
        self.table.attrib['class'] = 'fields'

        self.add_row()

        self.children = children

        for child in children:

            string = not child.nolabel and child.string
            rowspan = child.rowspan or 1
            colspan = child.colspan or 1

            self.add2(child, string, rowspan=rowspan, colspan=colspan)

    def add_row(self):
        tr = ET.Element('tr')
        self.table.append(tr)
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

        td = ET.Element('td')

        if rowspan: td.attrib['rowspan'] = str(rowspan)
        if colspan: td.attrib['colspan'] = str(colspan)
        if css_class: td.attrib['class'] = css_class

        if isinstance(widget, tg.widgets.Widget):
            td.append(widget.display())

            if isinstance(widget, Notebook):
                del self.table.attrib['class']

        else: # string
            td.text = widget + ":"

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

class Notebook(tg.widgets.CompoundWidget, TinyWidget):
    """Notebook widget, contains list of frames. Each frame will be displayed as a
    page of the the Notebook.
    """

    template = """
    <div class='tabber' xmlns:py="http://purl.org/kid/ns#">
        <div class='tabbertab' py:for="page in children">
            <h3>${page.string}</h3>
            <div>
                ${page.display()}
            </div>
        </div>
    </div>
    """

    member_widgets = ['_notebook_', "children"]
    _notebook_ = tg.widgets.Tabber()

    def __init__(self, attrs, children):
        TinyWidget.__init__(self, attrs)
        tg.widgets.CompoundWidget.__init__(self, name="Notebook")

        self.children = children
        self.nolabel = True

class Separator(tg.widgets.Widget, TinyWidget):
    """Separator widget.
    """

    params = ['string']
    template = "tinyerp.widgets.templates.separator"

    def __init__(self, attrs={}):
        TinyWidget.__init__(self, attrs)
        tg.widgets.Widget.__init__(self, name=self.name)

        self.colspan = 4
        self.rowspan = 1
        self.nolabel = True

class NewLine(tg.widgets.Widget, TinyWidget):
    """NewLine widget just tells the Frame widget to start new row during
    layout process.
    """
    template = "<span/>"

class Label(tg.widgets.FormField, TinyField):
    template = """<div style="text-align: center; width: 100%" xmlns:py="http://purl.org/kid/ns#">
        ${field_value}
    </div>
    """
    params = ["field_value"]

    def __init__(self, attrs={}):
        TinyField.__init__(self, attrs)
        tg.widgets.FormField.__init__(self, name=self.name)

        self.nolabel = True
        self.field_value = self.string

    def set_value(self, value):
        self.field_value = unicode(value or '', 'utf-8')

class Char(tg.widgets.FormField, TinyField):
    template = "tinyerp.widgets.templates.char"
    params = ["field_value"]

    def __init__(self, attrs={}):
        TinyField.__init__(self, attrs)
        tg.widgets.FormField.__init__(self, name=self.name)

    def set_value(self, value):
        self.field_value = unicode(value or '', 'utf-8')

class Text(tg.widgets.FormField, TinyField):
    template = "tinyerp.widgets.templates.text"
    params = ["field_value"]

    def __init__(self, attrs={}):
        TinyField.__init__(self, attrs)
        tg.widgets.FormField.__init__(self, name=self.name)

    def set_value(self, value):
        self.field_value = unicode(value or '', 'utf-8')

class Integer(tg.widgets.FormField, TinyField):
    template = "tinyerp.widgets.templates.integer"
    params = ["field_value"]

    def __init__(self, attrs={}):
        TinyField.__init__(self, attrs)
        tg.widgets.FormField.__init__(self, name=self.name)

    def set_value(self, value):
        if value:
            self.field_value = int(value)

class Boolean(tg.widgets.FormField, TinyField):
    template = "tinyerp.widgets.templates.boolean"
    params = ["field_value", "checked"]

    checked = {}

    def __init__(self, attrs={}):
        TinyField.__init__(self, attrs)
        tg.widgets.FormField.__init__(self, name=self.name)

    def set_value(self, value):
        self.field_value = value or ''

        if value:
            self.checked['checked'] = "1"

class Float(tg.widgets.FormField, TinyField):
    template = "tinyerp.widgets.templates.float"
    params = ["field_value"]

    def __init__(self, attrs={}):
        TinyField.__init__(self, attrs)
        tg.widgets.FormField.__init__(self, name=self.name)

class Selection(tg.widgets.FormField, TinyField):
    template = "tinyerp.widgets.templates.selection"
    params = ['options', 'field_value']
    options = []

    def __init__(self, attrs={}):
        TinyField.__init__(self, attrs)
        tg.widgets.FormField.__init__(self, name=self.name)

        self.options = attrs.get('selection', [])

class DateTime(tg.widgets.CalendarDatePicker, TinyField):
    template = "tinyerp.widgets.templates.datetime"
    params = ["format", "field_value"]
    format = "%Y-%m-%d %H:%M"
    picker_shows_time = True

    def __init__(self, attrs={}):
        TinyField.__init__(self, attrs)
        tg.widgets.CalendarDatePicker.__init__(self, name=self.name)

        if attrs['type'] == 'date':
            self.format = "%Y-%m-%d"
            self.picker_shows_time = False
        elif attrs['type'] == 'time':
            self.format = "%H:%M"

    def set_value(self, value):
        if hasattr(value, 'strftime'):
            self.field_value = value.strftime(self.format)
        elif value:
            self.field_value = value

class Button(tg.widgets.Widget, TinyWidget):
    """Button widget

    @todo: use states
    @todo: actions
    """

    template = """<button type="button" style="width: 100%" id="${name}" name="${name}">${string}</button>"""
    params = ["name", "string"]

    def __init__(self, attrs={}):
        TinyWidget.__init__(self, attrs)
        tg.widgets.Widget.__init__(self, name=self.name)

        self.nolabel = True

class Group(tg.widgets.CompoundWidget, TinyWidget):
    template = """
    <span xmlns:py="http://purl.org/kid/ns#">
        <fieldset py:if="string">
            <legend py:content="string" />
            ${frame.display()}
        </fieldset>
        <span py:replace="frame.display()" py:if="not string"/>
    </span>
    """

    params = ["string"]
    member_widgets = ["frame"]
    frame = None

    def __init__(self, attrs, children):
        TinyWidget.__init__(self, attrs)
        tg.widgets.CompoundWidget.__init__(self, name=self.name)

        self.frame = Frame(attrs, children, columns=int(attrs.get('col', 4)))
        self.nolabel = True

class M2O(tg.widgets.FormField, TinyField):
    template = "tinyerp.widgets.templates.many2one"
    params=['relation', 'field_value', 'text']

    def __init__(self, attrs={}):
        TinyField.__init__(self, attrs)
        self.relation = attrs.get('relation', '')

    def set_value(self, value):
        try:
            super(M2O, self).set_value(value[0])
            self.text = unicode(value[-1])
        except:
            pass

class O2M(tg.widgets.CompoundWidget, TinyWidget):
    """One2Many widget
    """
    template = "tinyerp.widgets.templates.one2many"
    params = ['string', 'id']

    member_widgets = ['form']
    form = None

    def __init__(self, attrs={}):
        TinyWidget.__init__(self, attrs)
        tg.widgets.CompoundWidget.__init__(self, name=self.name)

        #self.colspan = 4
        #self.nolabel = True

        self.model = attrs['relation']

        #XXX: if self.model == parent.model then goes in infinite loop (for example: mrp.bom)
        #TODO: generate view according to the view_mode (['form', 'tree'] or ['tree', 'form'])

        view = attrs['views'].get('form', None)

        id = attrs['value'] or None
        if id and len(id) > 0:
            id = id[0]

        self.form = Form(prefix=self.name, view_id=False, model=self.model, id=id, view_preloaded=view)

class M2M(tg.widgets.CompoundWidget, TinyWidget):
    """many2many widget

    @todo: implement me!!!
    """
    template = "tinyerp.widgets.templates.many2many"
    params = ['relation']

    def __init__(self, attrs={}):
        TinyWidget.__init__(self, attrs)
        self.relation = attrs.get('relation', '')

class Form(tg.widgets.CompoundWidget):
    """A generic form widget
    """

    template = """
    <span xmlns:py="http://purl.org/kid/ns#" py:replace="frame.display()" py:if="frame"/>
    """

    member_widgets = ['frame']
    frame = None

    def __init__(self, prefix, view_id, model, id=None, domain=[], view_ids=[], view_preloaded=None, context={}):
        """Create new instance of a Form.

        @param prefix: prefix for all the member fields
        @param view_id: the view id to load
        @param model: the model
        @param id: record id
        @param domain: the domain
        @param view_ids: view ids
        @param context: the context

        @return: a new instance of Form widget
        """

        proxy = rpc.RPCProxy(model)

        view = view_preloaded
        if not view:
            view = proxy.fields_view_get(view_id, 'form', context)

        fields = view['fields']

        dom = xml.dom.minidom.parseString(view['arch'])
        root = dom.childNodes[0]
        attrs = tools.node_attributes(root)
        self.string = attrs.get('string', '')

        values = {}

        try:
            if id :
                id = int(id)
                res = proxy.read([id], fields.keys())
                values = res[0]
            else: # default
                values = proxy.default_get(fields.keys())
        except Exception, e:
            message = str(e)

        self.frame = self.parse(prefix, model, dom, fields, values)[0]

    def parse(self, prefix='', model=None, root=None, fields=None, values={}):

        views = []

        for node in root.childNodes:

            if not node.nodeType==node.ELEMENT_NODE:
                continue

            attrs = tools.node_attributes(node)
            attrs['prefix'] = prefix

            if node.localName=='image':
                pass

            elif node.localName=='separator':
                wid = Separator(attrs)
                views += [wid]

            elif node.localName=='label':
                views += [Label(attrs)]

            elif node.localName=='newline':
                views += [NewLine()]

            elif node.localName=='button':
                views += [Button(attrs)]

            elif node.localName == 'form':
                n = self.parse(prefix=prefix, model=model, root=node, fields=fields, values=values)
                views += [Frame(attrs, n)]

            elif node.localName == 'notebook':
                n = self.parse(prefix=prefix, model=model, root=node, fields=fields, values=values)
                views += [Notebook(attrs, n)]

            elif node.localName == 'page':
                n = self.parse(prefix=prefix, model=model, root=node, fields=fields, values=values)
                views += [Frame(attrs, n)]

            elif node.localName=='group':
                n = self.parse(prefix=prefix, model=model, root=node, fields=fields, values=values)
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

                if isinstance(field, TinyField):
                    field.set_value(values.get(name, ''))

                views += [field]

        return views

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
