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

def to_local_datetime(text, server_format, local_format=None):
    
    local_format = local_format or server_format
    
    if not text:
        return ''
    
    date = time.strptime(text, server_format)
    if 'tz' in rpc.session.context:
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

    return time.strftime(local_format, date)

def to_server_datetime(text, server_format, local_format=None):
    local_format = local_format or server_format
    
    if not text:
        return False
    
    try:
        date = time.strptime(text, local_format)
    except:
        try:
            dt = list(time.localtime())
            dt[2] = int(text)
            date = tuple(dt)
        except:
            return False

    if 'tz' in rpc.session.context:
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

    return time.strftime(server_format, date)