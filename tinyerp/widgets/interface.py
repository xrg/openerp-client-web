###############################################################################
#
# Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id: list.py 7 2007-03-23 12:58:38Z ame $
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

    def __init__(self, attrs={}):

        self.string = attrs.get("string", None)
        self.model = attrs.get("model", None)

        prefix = attrs.get('prefix', '')
        self.name = prefix + (prefix and '/' or '') + attrs.get('name', '')

        self.colspan = int(attrs.get('colspan', 1))
        self.rowspan = int(attrs.get('rowspan', 1))

        self.select = int(attrs.get('select', 0))
        self.nolabel = int(attrs.get('nolabel', 0))
        self.required = int(attrs.get('required', 0))
        self.readonly = int(attrs.get('readonly', 0))

class TinyInputWidget(TinyWidget):
    """Interface for Field widgets, every InputField widget should
    implement this class
    """

    def __init__(self, attrs={}):
        TinyWidget.__init__(self, attrs)
        self._validator = None

    def get_validator(self):
        if self._validator:
            self._validator.not_empty = self.required
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
        self.default = value

    def update_params(self, d):
        super(TinyInputWidget, self).update_params(d)

        if self.readonly:
            d['field_class'] = " ".join([d['field_class'], "readonlyfield"])

        if self.required and 'requiredfield' not in d['field_class'].split(' '):
            d['field_class'] = " ".join([d['field_class'], "requiredfield"])

        if hasattr(self, 'error') and self.error:
            d['field_class'] = " ".join([d['field_class'], "errorfield"])

class TinyCompoundWidget(TinyInputWidget, tg.widgets.CompoundWidget):

    def __init__(self, attrs={}):
        TinyInputWidget.__init__(self, attrs)
        tg.widgets.CompoundWidget.__init__(self, name=self.name or None)

    def update_params(self, d):
        tg.widgets.CompoundWidget.update_params(self, d)

class TinyField(TinyInputWidget, tg.widgets.FormField):

    def __init__(self, attrs):
        TinyInputWidget.__init__(self, attrs)
        tg.widgets.FormField.__init__(self, name=self.name)


