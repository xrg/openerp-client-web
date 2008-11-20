###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

"""
This module defines validators.
"""
import re
import cgi
import math
import base64
import locale

import turbogears as tg

from openerp import tools
from openerp import format
from openerp import icons

class String(tg.validators.String):
    if_empty = False

    def _to_python(self, value, state):
        if isinstance(value, unicode):
            return value.encode('utf-8')

        return value

    def _from_python(self, value, state):
        return ustr(value or '')

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
    digit = 2

    def _from_python(self, value, state):
        return format.format_decimal(value or 0.0, self.digit)

    def _to_python(self, value, state):
        try:
            value = format.parse_decimal(value)
        except ValueError:
            pass
        return tg.validators.validators.Number.to_python(value, state)

class FloatTime(Float):
    
    if_empty = False
    
    def _from_python(self, value, state):
        val = value or 0.0
        t = '%02d:%02d' % (math.floor(abs(val)),round(abs(val)%1+0.01,2) * 60)
        if val < 0:
            t = '-' + t
        return t
    
    def _to_python(self, value, state):
        try:
            if value and ':' in value:
                return round(int(value.split(':')[0]) + int(value.split(':')[1]) / 60.0, 2)
            else:
                return locale.atof(value)
        except:
            pass
        
        return 0.0
    
class DateTime(tg.validators.DateTimeConverter):
    if_empty = False
    kind = "datetime"
    
    def __init__(self, kind="datetime", allow_empty = None, *args, **kwargs):
        super(DateTime, self).__init__(allow_empty=allow_empty, *args, **kwargs)       
        self.format = format.get_datetime_format(kind)
        self.kind = kind
    
    def _to_python(self, value, state):
        # do validation
        res = super(DateTime, self)._to_python(value, state)
        # return str instead of real datetime object
        return format.parse_datetime(value, kind=self.kind)

    def _from_python(self, value, state):
        return format.format_datetime(value, kind=self.kind)

class Selection(tg.validators.FancyValidator):
    if_empty = False

    def _to_python(self, value, state):

        if isinstance(value, basestring):
            if re.match('True|False|None', value):
                return eval(value)
            if re.match('^\-+|\d+$', value):
                return int(value)
            if re.match('^\-+|\d+(\.\d+)$', value):
                return float(value)

        return value

class Reference(tg.validators.FancyValidator):
    if_empty = False

    def _to_python(self, value, state):

        if isinstance(value, basestring):
            value = eval(value)

        id, ref = value
        if ref and id:
            return "%s,%d"%(ref, int(id))

        return False

class Binary(tg.validators.FancyValidator):
    if_empty = False

    def _to_python(self, value, state):
        if isinstance(value, cgi.FieldStorage):
            if value.filename:
                return base64.encodestring(value.file.read())
            elif self.not_empty:
                raise tg.validators.Invalid(_('Please select a file.'), value, state)

        return self.if_empty

class Url(tg.validators.URL):
    if_empty = False

    url_re = re.compile(r'(^(http|https|ftp|file)://(.*?:.*?@)?([^\s/:]+)(:\d+)?(/.*)?$)|^(http|https|ftp|file)://', re.IGNORECASE)

    def _from_python(self, value, state):
        return value or ''

class Email(tg.validators.Email):
    if_empty = False

    def _from_python(self, value, state):
        return value or ''

class many2many(tg.validators.FancyValidator):

    if_empty = [(6, 0, [])]

    def _to_python(self, value, state):

        if isinstance(value, basestring):
            value = eval(value)

        if not isinstance(value, (tuple, list)):
            value = (value or []) and [value]

        return [(6, 0, [int(id) for id in value if id])]

class many2one(tg.validators.FancyValidator):

    if_empty = False

    def _to_python(self, value, state):
        if isinstance(value, (list, tuple)):
            value = (len(value) or False) and value[0]

        try:
            return int(value)
        except:
            return False

    def _from_python(self, value, state):
        if isinstance(value, (list, tuple)):
            value = (len(value) or False) and value[0]

        return value


class Picture(tg.validators.FancyValidator):
    if_empty = False

    def _from_python(self, value, state):
        if isinstance(value, tuple):
            type, data = value
        else:
            type, data = 'jpeg', value

        if type == 'stock':
            stock, size = data
            url = icons.get_icon(stock)
        else:
            url = 'data:image/%s;base64,%s' % (type, data)
        return url

# vim: ts=4 sts=4 sw=4 si et

