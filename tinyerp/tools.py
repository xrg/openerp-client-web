###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
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
# along with this program; if not, write to the 
# Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
# Boston, MA  02111-1307, USA.
#
###############################################################################

import os
import time
import datetime as DT

from tinyerp import rpc

def expr_eval(string, context={}):
    context['uid'] = rpc.session.uid
    if isinstance(string, basestring):
        return eval(string, context)
    else:
        return string

def node_attributes(node):
   result = {}
   attrs = node.attributes
   if attrs is None:
       return {}
   for i in range(attrs.length):
           result[attrs.item(i).localName] = attrs.item(i).nodeValue
   return result

DT_SERVER_FORMATS = {
  'datetime' : '%Y-%m-%d %H:%M:%S',
  'date' : '%Y-%m-%d',
  'time' : '%H:%M:%S'
}

DT_LOCAL_FORMATS = {
  'datetime' : '%Y-%m-%d %H:%M:%S',
  'date' : '%Y-%m-%d',
  'time' : '%H:%M:%S'
}

def server_to_local_datetime(date, kind="datetime", as_timetuple=False):
    """Convert date value to the local datetime considering timezone info.

    @param date: the date value
    @param kind: type of the date value (date, time or datetime)
    @param as_timetuple: return timetuple
    
    @type date: basestring or time.time_tuple)
    
    @return: string or timetuple
    """

    server_format = DT_SERVER_FORMATS[kind]
    local_format = DT_LOCAL_FORMATS[kind]
    
    if not date:
        return ''
    
    if isinstance(date, time.struct_time):
        date = time.strftime(server_format, date)
        
    date = time.strptime(date, server_format)

    if kind == "datetime" and 'tz' in rpc.session.context:
        try:
            import pytz
            lzone = pytz.timezone(str(rpc.session.context['tz']))
            szone = pytz.timezone(str(rpc.session.timezone))
            dt = DT.datetime(date[0], date[1], date[2], date[3], date[4], date[5], date[6])
            sdt = szone.localize(dt, is_dst=True)
            ldt = sdt.astimezone(lzone)
            date = ldt.timetuple()
        except:
            pass

    if as_timetuple:
        return date
    
    return time.strftime(local_format, date)

def local_to_server_datetime(date, kind="datetime", as_timetuple=False):
    """Convert date value to the server datetime considering timezone info.

    @param date: the date value
    @param kind: type of the date value (date, time or datetime)
    @param as_timetuple: return timetuple
    
    @type date: basestring or time.time_tuple)
    
    @return: string or timetuple
    """
    
    server_format = DT_SERVER_FORMATS[kind]
    local_format = DT_LOCAL_FORMATS[kind]

    if not date:
        return False

    if isinstance(date, time.struct_time):
        date = time.strftime(local_format, date)

    try:
        date = time.strptime(date, local_format)
    except:
        try:
            dt = list(time.localtime())
            dt[2] = int(date)
            date = tuple(dt)
        except:
            return False

    if kind == "datetime" and 'tz' in rpc.session.context:
        try:
            import pytz
            lzone = pytz.timezone(rpc.session.context['tz'])
            szone = pytz.timezone(rpc.session.timezone)
            dt = DT.datetime(date[0], date[1], date[2], date[3], date[4], date[5], date[6])
            ldt = lzone.localize(dt, is_dst=True)
            sdt = ldt.astimezone(szone)
            date = sdt.timetuple()
        except:
            pass

    if as_timetuple:
        return date
    
    return time.strftime(server_format, date)

