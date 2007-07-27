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
import locale
import xml.dom.minidom

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp.cache import cache

from interface import TinyCompoundWidget

DT_FORMAT = '%Y-%m-%d'
DHM_FORMAT = '%Y-%m-%d %H:%M:%S'
HM_FORMAT = '%H:%M:%S'

if not hasattr(locale, 'nl_langinfo'):
    locale.nl_langinfo = lambda *a: '%x'

if not hasattr(locale, 'D_FMT'):
    locale.D_FMT = None

class Graph(TinyCompoundWidget):

    template = """
    <table width="100%">
        <tr>
            <td align="center">
                <img class="graph" src="${tg.query('/graph', _terp_model=model, _terp_view_id=view_id, _terp_ids=ustr(ids), _terp_domain=ustr(domain), _terp_context=ustr(context), width=width, height=height)}"/>
            </td>
        </tr>
    </table>
    """

    params = ['model', 'view_id', 'ids', 'domain', 'context', 'width', 'height']
    
    def __init__(self, model, view_id=False, ids=[], domain=[], context={}, width=400, height=400):

        self.model = model
        self.view_id = view_id
        self.ids = ids
        self.domain = domain
        self.context = context
        
        self.width = width
        self.height = height
        
        view = cache.fields_view_get(model, view_id, 'graph', rpc.session.context)
        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]
        attrs = tools.node_attributes(root)
        self.string = attrs.get('string', '')
                
        if ids is None:
            self.ids = rpc.RPCProxy(model).search(domain)

class GraphData(object):
    
    def __init__(self, model, view_id=False, ids=[], domain=[], context={}):
        
        view = cache.fields_view_get(model, view_id, 'graph', context)
        fields = view['fields']
        
        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]
                
        attrs = tools.node_attributes(root)
        
        self.string = attrs.get('string', 'Unknown')
        self.kind = attrs.get('type', 'pie')
        self.orientation = attrs.get('orientation', 'vertical')
        self.values = []
                
        axis, axis_data, axis_group = self.parse(root, fields)                       

        proxy = rpc.RPCProxy(model)

        if ids is None:
            ids = proxy.search(domain)

        ctx = rpc.session.context.copy()
        ctx.update(context)

        values = proxy.read(ids, fields.keys(), ctx)
        
        for value in values:
            res = {}
            for x in axis_data.keys():
                if fields[x]['type'] in ('many2one', 'char','time','text','selection'):
                    res[x] = value[x]
                    if isinstance(res[x], (list, tuple)):
                        res[x] = res[x][-1]
                    res[x] = str(res[x])
                elif fields[x]['type'] == 'date':
                    date = time.strptime(value[x], DT_FORMAT)
                    res[x] = time.strftime(locale.nl_langinfo(locale.D_FMT).replace('%y', '%Y'), date)
                elif fields[x]['type'] == 'datetime':
                    date = time.strptime(value[x], DHM_FORMAT)
                    if 'tz' in rpc.session.context:
                        try:
                            import pytz
                            lzone = pytz.timezone(rpc.session.context['tz'])
                            szone = pytz.timezone(rpc.session.timezone)
                            dt = DT.datetime(date[0], date[1], date[2], date[3], date[4], date[5], date[6])
                            sdt = szone.localize(dt, is_dst=True)
                            ldt = sdt.astimezone(lzone)
                            date = ldt.timetuple()
                        except:
                            pass
                    res[x] = time.strftime(locale.nl_langinfo(locale.D_FMT).replace('%y', '%Y')+' %H:%M:%S', date)
                else:
                    res[x] = float(value[x])
                    
            self.values.append(res)

        self.axis = axis
        self.axis_data = axis_data
        self.axis_group_field = axis_group

    def parse(self, root, fields):
        
        attrs = tools.node_attributes(root)

        axis = []
        axis_data = {}
        axis_group = {}

        for node in root.childNodes:
            attrs = tools.node_attributes(node)
            if node.localName == 'field':
                name = attrs['name']
                attrs['string'] = fields[name]['string']

                axis.append(str(name))
                axis_data[str(name)] =  attrs

        for i in axis_data:
            axis_data[i]['string'] = fields[i]['string']
            if axis_data[i].get('group', False):
                axis_group[i]=1
                axis.remove(i)
                
        return axis, axis_data, axis_group
            