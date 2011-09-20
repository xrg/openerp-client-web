###############################################################################
#
#  Copyright (C) 2007-TODAY OpenERP SA. All Rights Reserved.
#
#  $Id$
#
#  Developed by OpenERP (http://openerp.com) and Axelor (http://axelor.com).
#
#  The OpenERP web client is distributed under the "OpenERP Public License".
#  It's based on Mozilla Public License Version (MPL) 1.1 with following 
#  restrictions:
#
#  -   All names, links and logos of OpenERP must be kept as in original
#      distribution without any changes in all software screens, especially
#      in start-up page and the software header, even if the application
#      source code has been changed or updated or code has been added.
#
#  You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################
import datetime as DT
import re
import time

import cherrypy
import pytz
from babel import dates, numbers

from openobject.i18n.utils import get_locale
#from openerp.utils import cache
#from openerp.utils import rpc

__all__ = ['DT_SERVER_FORMATS', 'get_datetime_format',
           'format_datetime', 'parse_datetime',
           'format_decimal', 'parse_decimal',
           'tz_convert'
          ]

DT_SERVER_FORMATS = {
  'datetime' : '%Y-%m-%d %H:%M:%S',
  'date' : '%Y-%m-%d',
  'time' : '%H:%M:%S'
}

__pat = re.compile("%\(([dMy]+)\)s")
__sub = {'d': '%d', 'M': '%m', 'y': '%Y'}
def _to_posix_format(format):
    """Convert LDML format string to posix format string.
    """
    return __pat.sub(lambda m: __sub[m.group(1)[0]], format)

def format_date_custom(dt, fmt="y-M-d"):
    return dates.format_date(dt, format=fmt, locale=get_locale())

def get_datetime_format(kind="datetime"):
    """Get local datetime format.

    @param kind: type (date, time or datetime)
    @return: string

    @todo: cache formats to improve performance.
    """
    if 'lang' in cherrypy.session:
        # server-defined formatting
        if kind == 'time':
            return cherrypy.session['lang']['time_format']
        elif kind == 'date':
            return cherrypy.session['lang']['date_format']
        else:
            return "%(date_format)s %(time_format)s"% cherrypy.session['lang']

    # TODO: correctly convert from LDML to POSIX datetime formatting
    # current converter is trivial and lame and probably very easy to break
    date_format = _to_posix_format(dates.get_date_format(
            format='short', locale=get_locale())).format
    if kind == 'time':
        # Should use dates.get_time_format(locale=get_locale())
        return '%H:%M:%S'
    elif kind == 'date':
        return date_format
    else:
        # Should use dates.get_datetime_format, but that one returns
        # a 2.6-style formats
        return "%s %s" % (date_format, '%H:%M:%S')

def tz_convert(struct_time, action):
    # if no client timezone is configured, consider the client is in the same
    # timezone as the server
    lzone = pytz.timezone(cherrypy.session['client_timezone']
                          or cherrypy.session['remote_timezone'])
    szone = pytz.timezone(cherrypy.session['remote_timezone'])
    dt = DT.datetime.fromtimestamp(time.mktime(struct_time))

    if action == 'parse':
        fromzone = lzone
        tozone = szone
    elif action == 'format':
        fromzone = szone
        tozone = lzone
    else:
        raise Exception("_tz_convert action should be 'parse' or 'format'. Not '%s'" % (action, ))

    localized_original_datetime = fromzone.localize(dt, is_dst=True)
    destination_datetime = localized_original_datetime.astimezone(tozone)
    return destination_datetime.timetuple()

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
            value = tz_convert(value, 'format')
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
    except ValueError:
        try:
            # might be in server format already (e.g. filter domain)
            value = time.strptime(value, server_format)
        except ValueError:
            try:
                dt = list(time.localtime())
                dt[2] = int(value)
                value = tuple(dt)
            except:
                return False

    if kind == "datetime":
        try:
            value = tz_convert(value, 'parse')
        except Exception:
            cherrypy.log.error("Error in timezone parsing:\n", traceback=True)

    if as_timetuple:
        return value

    return time.strftime(server_format, value)

def convert_date_format_in_domain(domain, fields, context):
    try:
        return _convert_date_format_in_domain(domain, fields, context)
    except Exception, e:
        cherrypy.log.error("Error in convert_date_format_in_domain:\n", traceback=True)
        return domain

def _convert_date_format_in_domain(domain, fields, context):
    from view_calendar.widgets.utils import DT_FORMAT_INFO
    from openerp.utils import rpc

    date_fields = dict([(field_name, field_def['type'])
                            for field_name, field_def
                                in fields.items()
                                    if field_def['type'] in ['date', 'datetime', 'time']])

    if 'lang' not in cherrypy.session:
        return domain
    lang_def = cherrypy.session['lang']
    fixed_domain = []

    # not supported on all systems: %C %D %e %F %g %G %h %l %P %r %R %s %T %u %V %z
    time_format_convert_map = {
        '%D': '%m/%d/%y',
        '%e': '%d',
        '%F': '%Y-%m-%d',
        '%g': '%y',
        '%h': '%b',
        '%l': '%I',
        '%P': '%p',
        '%R': '%H:%M',
        '%r': '%I:%M:%S %p',
        '%T': '%H:%M:%S',
        '%z': '%Z',
    }

    for item in domain:
        if len(item) != 3:
            fixed_domain.append(item)
        else:
            key, op, val = item
            if key in date_fields:
                dtype = date_fields[key]
                if dtype == 'date':
                    user_dformat = lang_def['date_format']
                    server_dformat = DT_FORMAT_INFO['date'][0]
                elif dtype == 'time':
                    user_dformat = lang_def['time_format']
                    server_dformat = DT_FORMAT_INFO['time'][0]
                elif dtype == 'datetime':
                    user_dformat = lang_def['date_format'] + ' ' + lang_def['time_format']
                    server_dformat = DT_FORMAT_INFO['datetime'][0]

                ok = True
                for k, v in time_format_convert_map.items():
                    if k in user_dformat:
                        user_dformat = user_dformat.replace(k, v)
                if re.findall(r'%[CGsuV]', user_dformat):
                    ok = False

                value_is_list = isinstance(val, list)
                if value_is_list:
                    val = val[0]

                if ok:
                    val = parse_datetime(val, dtype)
                    if val:
                        val = DT.datetime.strptime(
                                DT.datetime.strptime(val, server_dformat)\
                                    .strftime(user_dformat), user_dformat)\
                            .strftime(server_dformat)
                    else:
                        formated_date = format_datetime(val, dtype)
                        val = parse_datetime(formated_date, dtype)
                        if val:
                            val = DT.datetime.strptime(
                                    DT.datetime.strptime(val, server_dformat)\
                                        .strftime(user_dformat), user_dformat)\
                                .strftime(server_dformat)
                if value_is_list:
                    val = [val]
            fixed_domain.append((key, op, val))

    return fixed_domain

LOCALE_CACHE = {
               'date_format':'%m/%d/%Y',
               'time_format':'%H:%M:%S',
               'grouping':[],
               'decimal_point':'.',
               'thousands_sep': ','
                }

def get_lang_float_format(locale_lang,monetary=False):
    thousands_sep = LOCALE_CACHE.get('thousands_sep') or numbers.get_group_symbol(locale_lang)
    decimal_point = LOCALE_CACHE.get('decimal_point')
    grouping      = LOCALE_CACHE.get('grouping')
    return (grouping, thousands_sep, decimal_point)


def format_decimal(value, digits=2, grouping=True, monetary=False):
    locale = get_locale()
    formatted = ("%%.%df" % digits) % value
    lang_grouping, thousands_sep, decimal_point = get_lang_float_format(locale,monetary=False)
    
    seps = 0
    parts = formatted.split('.')

    if grouping:
        parts[0], seps = group(parts[0], monetary=monetary, grouping=lang_grouping, thousands_sep=thousands_sep)

    formatted = decimal_point.join(parts)
    while seps:
        sp = formatted.find(' ')
        if sp == -1: break
        formatted = formatted[:sp] + formatted[sp+1:]
        seps -= 1
    return formatted


def group(value, monetary=False, grouping=False, thousands_sep=''):

    """ This function will convert the value in appropriate format after applying
        thousands_sep, grouping etc

        @param value:The value to be converted
        @param monetary:True or False by default False
        @param grouping:True or False by default False
        @param thousands_sep: The symbol to be applied at the thousand's place by default blank

        @return: The converted value"""

    grouping = eval(grouping)
    if not grouping:
        return (value, 0)

    result = ""
    seps = 0
    spaces = ""

    if value[-1] == ' ':
        sp = value.find(' ')
        spaces = value[sp:]
        value = value[:sp]

    while value and grouping:
        # if grouping is -1, we are done
        if grouping[0] == -1:
            break
        # 0: re-use last group ad infinitum
        elif grouping[0] != 0:
            #process last group
            group = grouping[0]
            grouping = grouping[1:]
        if result:
            result = value[-group:] + thousands_sep + result
            seps += 1
        else:
            result = value[-group:]
        value = value[:-group]
        if value and value[-1] not in "0123456789":
            # the leading string is only spaces and signs
            return value + result + spaces, seps
    if not result:
        return value + spaces, seps
    if value:
        result = value + thousands_sep + result
        seps += 1
    return result + spaces, seps         
        

def set_locale_cache(lang_data={}):
    try:
        if lang_data:
            if 'id' in lang_data:
                del lang_data['id']
            LOCALE_CACHE.update(lang_data)
    except:
        pass

    
def parse_decimal(value):
    
    locale = get_locale()
    if isinstance(value, basestring):
        
        value = ustr(value)
        
        grouping, thousands_sep, decimal_point = get_lang_float_format(locale,monetary=False)
        #deal with ' ' instead of u'\xa0' (SP instead of NBSP as grouping char)
        value = value.replace(' ', '')
        value = value.replace(thousands_sep, '').replace(decimal_point, '.')

    if not isinstance(value, float):
        return float(value)

    return value
