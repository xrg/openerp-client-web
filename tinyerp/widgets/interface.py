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

    def __init__(self, attrs={}):

        self.string = attrs.get("string", None)
        self.model = attrs.get("model", None)

        prefix = attrs.get('prefix', '')
        self.name = prefix + (prefix and '/' or '') + attrs.get('name', '')

        self.colspan = int(attrs.get('colspan', 1))
        self.rowspan = int(attrs.get('rowspan', 1))
        self.select = int(attrs.get('select', 0))
        self.nolabel = int(attrs.get('nolabel', 0))

class TinyInputWidget(TinyWidget):
    """Interface for Field widgets, every InputField widget should
    implement this class
    """

    field_value = None

    def __init__(self, attrs={}):
        TinyWidget.__init__(self, attrs)

        self._validators = []

        if attrs.get('required', False):
            self._validators += [tg.validators.NotEmpty]

    def get_validator(self):
        if self._validators:
            return tg.validators.All(*self._validators)

        return None

    def set_validator(self, value):
        if value:
            self._validators = [value]

    def add_validator(self, value):
        self._validators += [value]

    validator = property(get_validator, set_validator)

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

    def update_params(self, d):
        super(TinyInputWidget, self).update_params(d)

class TinyCompoundWidget(TinyInputWidget, tg.widgets.CompoundWidget):

    def __init__(self, attrs={}):
        TinyInputWidget.__init__(self, attrs)
        tg.widgets.CompoundWidget.__init__(self, name=self.name or None)

class TinyField(TinyInputWidget, tg.widgets.FormField):
    def __init__(self, attrs):
        TinyInputWidget.__init__(self, attrs)
        tg.widgets.FormField.__init__(self, name=self.name)

