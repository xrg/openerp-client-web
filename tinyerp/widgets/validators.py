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
This module defines validators.
"""

import turbogears as tg

class Bool(tg.validators.FancyValidator):

    values = ['1', 'true']

    if_empty = False

    def _to_python(self, value, state):
        value = value or False
        if value:
            value = str(value).lower() in self.values

        return value

    def _from_python(self, value, state):
        return (value or '') and 1

class Int(tg.validators.Int):
    if_empty = False

class Float(tg.validators.Number):
    if_empty = False

    def _from_python(self, value, state):
        return value or 0.0

class DateTime(tg.validators.DateTimeConverter):
    if_empty = False

    def _to_python(self, value, state):
        res = super(DateTime, self)._to_python(value, state)
        # return str instead of real datetime object
        return value

class Selection(tg.validators.FancyValidator):
    if_empty = False

class many2many(tg.validators.FancyValidator):

    if_empty = [(6, 0, [])]

    def _to_python(self, value, state):

        if isinstance(value, basestring):
            value = eval(value)

        if not isinstance(value, list):
            value = (value or []) and [value]

        return [(6, 0, [int(id) for id in value])]
