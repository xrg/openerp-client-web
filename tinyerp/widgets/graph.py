###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://tinyerp.com) and Axelor (http://axelor.com).
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
import locale
import xml.dom.minidom
import urllib

import turbogears as tg

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common
from tinyerp import cache

from tinyerp.OpenFlashChart import graph as OFChart

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
                <div id="test" style="width: 500; height: 400"></div>
                <script type="text/javascript">
                    var so = new SWFObject("/static/open-flash-chart.swf", "ofc", "500", "400", "9", "#FFFFFF");
                    so.addVariable("data", "${tg.quote_plus(tg.url('/graph', _terp_model=model, _terp_view_id=view_id, _terp_ids=ustr(ids), _terp_domain=ustr(domain), _terp_context=ustr(context)))}");
                    so.addParam("allowScriptAccess", "sameDomain");
                    so.write("test");
                </script>
            </td>
        </tr>
    </table>
    """

    javascript = [tg.widgets.JSLink("tinyerp", "javascript/swfobject.js")]
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
            
colorline = ['#%02x%02x%02x' % (25+((r+10)%11)*23,5+((g+1)%11)*20,25+((b+4)%11)*23) for r in range(11) for g in range(11) for b in range(11) ]
def choice_colors(n):
    if n:
        return colorline[0:-1:len(colorline)/(n+1)]
    return []
    
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
        
        ctx = rpc.session.context.copy()
        ctx.update(context)

        if ids is None:
            ids = proxy.search(domain, 0, 0, 0, ctx)

        values = proxy.read(ids, fields.keys(), ctx)
        
        for value in values:
            res = {}
            for x in axis_data.keys():
                if fields[x]['type'] in ('many2one', 'char','time','text','selection'):
                    res[x] = value[x]
                    if isinstance(res[x], (list, tuple)):
                        res[x] = res[x][-1]
                    res[x] = ustr(res[x])
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

                axis.append(ustr(name))
                axis_data[ustr(name)] =  attrs

        for i in axis_data:
            axis_data[i]['string'] = fields[i]['string']
            if axis_data[i].get('group', False):
                axis_group[i]=1
                axis.remove(i)
                
        return axis, axis_data, axis_group
    
    def __str__(self):
        
        axis = self.axis
        axis_data = self.axis_data
        datas = self.values
        kind = self.kind
        
        operators = {
            '+': lambda x,y: x+y,
            '*': lambda x,y: x*y,
            'min': lambda x,y: min(x,y),
            'max': lambda x,y: max(x,y),
            '**': lambda x,y: x**y
        }
        
        keys = {}
        data_axis = {}
        label = {}
        lbl = []
        label_x = []
        
        for field in axis[1:]:
            
            for val in datas:
                lbl = val[axis[0]]
                key = urllib.quote_plus(val[axis[0]])
                info = data_axis.setdefault(key, {})
                keys[key] = 1
                label[lbl] = 1
                
                if field in info:
                    oper = operators[axis_data[field].get('operator', '+')]
                    info[field] = oper(info[field], val[field])
                else:
                    info[field] = val[field]
                    
        keys = keys.keys()
        keys.sort()
        
        label = label.keys()
        label.sort()
        
        for l in label:
            if(len(l) > 10):
                label_x.append(l.split('/')[-1])
            else:
                label_x.append(l)
                
        values = {}
        for field in axis[1:]:
            values[field] = map(lambda x: data_axis[x][field], keys)
    
        chart = OFChart()
        colors = choice_colors(len(axis))
        if kind == 'pie':
            value = []
            total = 0
            value = values.values()[0]
            
            for i in value:
                total = total+i
            
            val = []
            
            for j in value:
                val.append(round((j*100)/total))
                    
            colours = colors
            chart.pie_chart(70, 'red', 'blue')
            chart.pie_data(val, label_x, colours, 60)
            
        elif kind == 'bar':
            temp_lbl = []
            for i in label_x:
                temp_lbl.append(urllib.quote_plus(i))
                
            chart.set_x_labels(temp_lbl)
            chart.set_x_label_style(10, orientation=2)
            
            mx = 10
            for i, x in enumerate(axis[1:]):
                title = x
                data = values[x]
                
                chart.bar(80, colors[i], colors[i], title)
                chart.set_data(data)
                
                mx = max(mx, *data)
                chart.set_y_max(mx)
            
                #mx = math.floor(math.log10(mx)) * 100
                #chart.set_y_max(mx)
                #chart.y_label_steps(mx / 10)

        return chart.render()
