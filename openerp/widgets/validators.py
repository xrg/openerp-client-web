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

class URL(tg.validators.URL):

    if_empty = False
    require_tld = False

    url_re = re.compile(r'''
        ^(http|https|ftp|sftp|file)://          # protocol
        (?:[%:\w]*@)?                           # authenticator
        (?P<domain>[a-z0-9][a-z0-9\-]{1,62}\.)* # (sub)domain - alpha followed by 62max chars (63 total)
        (?P<tld>[a-z]{2,})?                     # TLD
        (?::[0-9]+)?                            # port

        # files/delims/etc
        (?P<path>/[a-z0-9\-\._~:/\?#\[\]@!%\$&\'\(\)\*\+,;=]*)?
        $
    ''', re.I | re.VERBOSE)

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





# Let some FormEncode strings goes into message catalog.
__email_messages = {
    'empty': _('Please enter an email address'),
    'noAt': _('An email address must contain a single @'),
    'badUsername': _('The username portion of the email address is invalid (the portion before the @: %(username)s)'),
    'badDomain': _('The domain portion of the email address is invalid (the portion after the @: %(domain)s)'),
}

__url_messages = {
    'noScheme': _('You must start your URL with http://, https://, etc'),
    'badURL': _('That is not a valid URL'),
    'noTLD': _('You must provide a full domain name (like %(domain)s.com)'),
}

__type_messages = {
    'integer': _("Please enter an integer value"),
    'number': _("Please enter a number"),
    'badFormat': _('Invalid datetime format'),
}

# vim: ts=4 sts=4 sw=4 si et

