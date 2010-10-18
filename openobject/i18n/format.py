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

import re
import time
import datetime as DT
import pytz
import cherrypy

from babel import dates
from babel import numbers
from babel.support import Format


from openobject.i18n.utils import get_locale

__all__ = ['get_datetime_format', 'format_datetime', 'parse_datetime', 'format_decimal', 'parse_decimal']

DT_SERVER_FORMATS = {
  'datetime' : '%Y-%m-%d %H:%M:%S',
  'date' : '%Y-%m-%d',
  'time' : '%H:%M:%S'
}

__pat = re.compile("\%\(([dMy]+)\)s")
__sub = {'d': '%d', 'M': '%m', 'y': '%Y'}
def _to_posix_format(format):
    """Convert LDML format string to posix format string.
    """
    return __pat.sub(lambda m: __sub[m.group(1)[0]], format)

def get_datetime_format(kind="datetime"):
    """Get local datetime format.

    @param kind: type (date, time or datetime)
    @return: string

    @todo: cache formats to improve performance.
    @todo: extend user preferences to allow customisable date format (tiny server).
    """

    fmt = "%H:%M:%S"

    if kind != "time":
        fmt =  dates.get_date_format("short", locale=get_locale()).format
        fmt = _to_posix_format(fmt)

    if kind == "datetime":
        fmt += " %H:%M:%S"

    return fmt

def _tz_convert(value, action):
    lzone = pytz.timezone(cherrypy.session['client_timezone'])
    szone = pytz.timezone(cherrypy.session['remote_timezone'])
    dt = DT.datetime(value[0], value[1], value[2], value[3], value[4], value[5], value[6])

    if action == 'parse':
        fromzone = lzone
        tozone = szone
    elif action == 'format':
        fromzone = szone
        tozone = lzone
    else:
        raise Exception("_tz_convert action should be 'parse' or 'format'. Not '%s'" % (action, ))

    fromdt = fromzone.localize(dt, is_dst=True)
    todt = fromdt.astimezone(tozone)
    value = todt.timetuple()

    return value

def format_datetime(value, kind="datetime", as_timetuple=False):
    """Convert date value to the local datetime considering timezone info.

    @param value: the date value
    @param kind: type of the date value (date, time or datetime)
    @param as_timetuple: return timetuple

    @type value: basestring or time.time_tuple)

    @return: string or timetuple
    """

    server_format = DT_SERVER_FORMATS[kind]
    local_format = get_datetime_format(kind)

    if not value:
        return ''

    if isinstance(value, (time.struct_time, tuple)):
        value = time.strftime(server_format, value)

    if isinstance(value, DT.datetime):
        value = ustr(value)
        try:
            value = DT.datetime.strptime(value[:10], server_format)
            return value.strftime(local_format)
        except:
            return ''

    value = value.strip()

    # remove trailing miliseconds
    value = re.sub("(.*?)(\s+\d{2}:\d{2}:\d{2})(\.\d+)?$", "\g<1>\g<2>", value)

    # add time part in value if missing
    if kind == 'datetime' and not re.search('\s+\d{2}:\d{2}:\d{2}?$', value):
        value += ' 00:00:00'

    # remove time part from value
    elif kind == 'date':
        value = re.sub('\s+\d{2}:\d{2}:\d{2}(\.\d+)?$', '', value)

    value = time.strptime(value, server_format)

    if kind == "datetime":
        try:
            value = _tz_convert(value, 'format')
        except Exception:
            cherrypy.log.error("Error in timezone formatting:\n", traceback=True)

    if as_timetuple:
        return value

    return time.strftime(local_format, value)

def parse_datetime(value, kind="datetime", as_timetuple=False):
    """Convert date value to the server datetime considering timezone info.

    @param value: the date value
    @param kind: type of the date value (date, time or datetime)
    @param as_timetuple: return timetuple

    @type value: basestring or time.time_tuple)

    @return: string or timetuple
    """

    server_format = DT_SERVER_FORMATS[kind]
    local_format = get_datetime_format(kind)

    if not value:
        return False

    if isinstance(value, (time.struct_time, tuple)):
        value = time.strftime(local_format, value)

    try:
        value = time.strptime(value, local_format)
    except:
        try:
            dt = list(time.localtime())
            dt[2] = int(value)
            value = tuple(dt)
        except:
            return False

    if kind == "datetime":
        try:
            value = _tz_convert(value, 'parse')
        except Exception:
            cherrypy.log.error("Error in timezone parsing:\n", traceback=True)

    if as_timetuple:
        return value

    return time.strftime(server_format, value)

def format_decimal(value, digits=2):
    locale = get_locale()
    v = ("%%.%df" % digits) % value
    if digits == 0:
        return numbers.format_number(value, locale=locale)
    num, decimals = v.split(".", 1)

    if num == "-0":
        val = "-0"
    else:
        val = numbers.format_number(int(num), locale=locale)

    return val + unicode(numbers.get_decimal_symbol(locale) + decimals)

def parse_decimal(value):

    if isinstance(value, basestring):

        value = ustr(value)

        #deal with ' ' instead of u'\xa0' (SP instead of NBSP as grouping char)
        value = value.replace(' ', '')
        try:
            value = numbers.parse_decimal(value, locale=get_locale())
        except ValueError, e:
            pass

    if not isinstance(value, float):
        return float(value)

    return value

# vim: ts=4 sts=4 sw=4 si et

