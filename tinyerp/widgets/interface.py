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

import turbogears as tg
import cherrypy

from tinyerp import tools

class TinyWidget(object):
    """Widget interface, every widget class should implement
    this class.
    """

    colspan = 1
    rowspan = 1
    string = None
    nolabel = False
    select = False
    required = False
    readonly = False
    help = None
    editable = True
    
    name = None
    model = None
    states = None
    callback = None
    kind=None

    def __init__(self, attrs={}):

        self.string = attrs.get("string", None)
        self.model = attrs.get("model", None)

        prefix = attrs.get('prefix', '')
        self.name = prefix + (prefix and '/' or '') + attrs.get('name', '')

        self.states = attrs.get('states', None)
        if isinstance(self.states, basestring):
            self.states = self.states.split(',')

        self.colspan = int(attrs.get('colspan', 1))
        self.rowspan = int(attrs.get('rowspan', 1))

        self.select = tools.expr_eval(attrs.get('select', False))
        self.nolabel = tools.expr_eval(attrs.get('nolabel', False))
        self.required = tools.expr_eval(attrs.get('required', False))
        self.readonly = tools.expr_eval(attrs.get('readonly', False))

        self.help = attrs.get('help')
        self.editable = attrs.get('editable', True)
        
        if 'state' in attrs:
            self.set_state(attrs['state'])

        self.callback = attrs.get('on_change', None)
        self.kind = attrs.get('type', None)

    def set_state(self, state):
        if isinstance(self.states, dict) and state in self.states:
            attrs = self.states[state]

            for n,v in attrs:
                setattr(self, n, v)

class TinyInputWidget(TinyWidget):
    """Interface for Field widgets, every InputField widget should
    implement this class
    """

    def __init__(self, attrs={}):
        TinyWidget.__init__(self, attrs)
        self._validator = None

    def get_validator(self):
        if self._validator:
            self._validator.not_empty = (self.required or False) and True
        elif self.required:
            self._validator = tg.validators.NotEmpty()

        return self._validator

    def set_validator(self, value):
        self._validator = value

    validator = property(get_validator, set_validator)

    def get_value(self):
        """Get the value of the field.

        @return: field value
        """
        return self.value

    def set_value(self, value):
        """Set the value of the field.

        @param value: the value
        """
        if isinstance(value, basestring):
            value = ustr(value)

        self.default = value

    def update_params(self, d):
        super(TinyInputWidget, self).update_params(d)
        d['attrs'] = {}
        # name as field_id
        d['field_id'] = self.name

        d['callback'] = self.callback
        d['onchange'] = (self.callback or None) and 'onChange(this)'

        d['kind'] = self.kind
        d['editable'] = self.editable
        
        if self.help:
            d['attrs']['title'] = self.help

        if self.readonly:
            d['field_class'] = " ".join([d['field_class'], "readonlyfield"])
            d['attrs']['disabled'] = True

        if self.required and 'requiredfield' not in d['field_class'].split(' '):
            d['field_class'] = " ".join([d['field_class'], "requiredfield"])

        if hasattr(self, 'error') and self.error:
            d['field_class'] = " ".join([d['field_class'], "errorfield"])

class TinyCompoundWidget(TinyInputWidget, tg.widgets.CompoundWidget):

    def __init__(self, attrs={}):
        TinyInputWidget.__init__(self, attrs)
        tg.widgets.CompoundWidget.__init__(self, name=self.name or None)
        
    def get_widgets_by_name(self, name, kind=tg.widgets.Widget, parent=None):
        result = []        
        parent = parent or self

        for wid in parent.iter_member_widgets():
            
            if wid.name == name and isinstance(wid, kind):
                result.append(wid)
                
            if isinstance(wid, tg.widgets.CompoundWidget):
                result += self.get_widgets_by_name(name, kind=kind, parent=wid)
        
        return result

    def update_params(self, d):
        tg.widgets.CompoundWidget.update_params(self, d)
        d['editable'] = self.editable

class TinyField(TinyInputWidget, tg.widgets.FormField):

    def __init__(self, attrs):
        TinyInputWidget.__init__(self, attrs)
        tg.widgets.FormField.__init__(self, name=self.name)


