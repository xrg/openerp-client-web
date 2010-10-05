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
# -   All names, links and logos of Tiny, OpenERP and Axelor must be
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
import base64
import cgi
import locale
import math
import re
import time

import formencode.validators
import formencode.api

from openobject.validators import BaseValidator
from openobject.i18n import format

class String(BaseValidator):
    if_empty = False

    def _to_python(self, value, state):
        if isinstance(value, unicode):
            return value.encode('utf-8')

        return value

    def _from_python(self, value, state):
        return ustr(value or '')

class Bool(BaseValidator):
    values = ['1', 'true']

    if_empty = False

    def _to_python(self, value, state):
        value = value or False
        if value:
            value = str(value).lower() in self.values

        return value

    def _from_python(self, value, state):
        return (value or '') and 1

class Int(formencode.validators.Int):
    if_empty = False

class Float(formencode.validators.Number):
    if_empty = False
    digit = 2

    def _from_python(self, value, state):
        return format.format_decimal(float(value) or 0.0, self.digit)

    def _to_python(self, value, state):
        try:
            value = format.parse_decimal(value)
        except ValueError:
            raise formencode.api.Invalid(_('Invalid literal for float'), value, state)
        return value

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

class DateTime(BaseValidator):
    if_empty = False
    kind = "datetime"

    def __init__(self, kind="datetime", *args, **kwargs):
        super(DateTime, self).__init__(*args, **kwargs)
        self.format = format.get_datetime_format(kind)
        self.kind = kind

    def _to_python(self, value, state):
        # do validation
        try:
            res = time.strptime(value, self.format)
        except ValueError:
            raise formencode.api.Invalid(_('Invalid datetime format'), value, state)
        # return str instead of real datetime object
        try:
            return format.parse_datetime(value, kind=self.kind)
        except ValueError:
            raise formencode.api.Invalid(_('Invalid datetime format'), value, state)

    def _from_python(self, value, state):
        return format.format_datetime(value, kind=self.kind)


class Selection(BaseValidator):
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

class Reference(BaseValidator):
    if_empty = False

    def _to_python(self, value, state):

        if isinstance(value, basestring):
            value = eval(value)

        id, ref = value
        if ref and id:
            return "%s,%d"%(ref, int(id))

        return False

class Binary(BaseValidator):
    if_empty = False

    def _to_python(self, value, state):

        if isinstance(value, list):
            value = value[0]

        if isinstance(value, cgi.FieldStorage):
            if value.filename:
                return base64.encodestring(value.file.read())
            elif self.not_empty:
                raise formencode.api.Invalid(_('Please select a file.'), value, state)
        elif value:
            return value
        return self.if_empty

class URL(formencode.validators.URL):

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

class Email(formencode.validators.Email):
    if_empty = False
    
    domainRE = re.compile(r'''
        (^(?:[a-z0-9][a-z0-9\-]{0,62}\.)+ # (sub)domain - alpha followed by 62max chars (63 total)
        [a-z]{2,}[\s,.]*$)*                     # TLD
    ''', re.I | re.VERBOSE)

    def _from_python(self, value, state):
        return value or ''

    def validate_python(self, value, state):
        if '<' in value and '>' in value:
            value = value[value.index('<') + 1:value.index('>')]
        super(Email, self).validate_python(value, state)

class many2many(BaseValidator):

    if_empty = [(6, 0, [])]

    def _to_python(self, value, state):

        if isinstance(value, basestring):
            value = eval(value)

        if not isinstance(value, (tuple, list)):
            value = (value or []) and [value]

        return [(6, 0, [int(id) for id in value if id])]

class many2one(BaseValidator):

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

        return value or ''
    
class one2many(formencode.validators.FancyValidator):
    
    if_empty = []


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
