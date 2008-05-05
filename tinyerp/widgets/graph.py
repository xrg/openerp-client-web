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
        
        cxt =  rpc.session.context.copy()
        cxt.update(context or {})
        
        view = cache.fields_view_get(model, view_id, 'graph', cxt)
        
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
        
        self.model = model
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

        rec_ids = []
        values = proxy.read(ids, fields.keys(), ctx)
        
        for value in values:
            res = {}
            rec_ids.append(value.get('id'))
            res['temp_id'] = value.get('id')
            
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
            
            res['id'] = value[axis[0]][0]
            res['rec_id'] = rec_ids
                    
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
        temp = {}
        
        lbl = []
        label_x = []        
        links = []
        total_ids = []
        dm = []
        domain = []
        lines = []
        
        for field in axis[1:]:
            
            for val in datas:
                key_ids = {}
                  
                key_ids['id'] = val.get('id')
                key_ids['rec_id'] = val.get('rec_id')
                
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
                    
                total_ids += [key_ids]
            
            for i in total_ids:
                dm = i.get('id')                
                temp[dm] = 1
                
        keys = keys.keys()
        keys.sort()
        
        label = label.keys()
        label.sort()
        
        temp = temp.keys()
        temp.sort()
        
        for field in axis[1:]:
            for d in temp:
                for val in datas:
                    rec = val.get('rec_id')
                
                domain += [(axis[0], '=', d), ('id', 'in', rec)]
                
        dom = []
        
        for d in domain:
            dom.append(urllib.quote_plus(str(d)))
            
        for l in label:
            if(len(l) > 10):
                label_x.append(l.split('/')[-1])
            else:
                label_x.append(l)
                
        values = {}
        for field in axis[1:]:
            values[field] = map(lambda x: data_axis[x][field], keys)
    
        colors = choice_colors(len(axis))
        if kind == 'pie':            
            
            tmp = ''
            
            pie = ''
            pie_values = ''
            pie_colours = ''
            pie_labels = ''
            pie_links = ''
            pie_label_size = 10
            pie_tool_tip = ''
            gradient = True
            border_size = -1
            
            proxy = rpc.RPCProxy(self.model)
            res = proxy.search(domain)
            
            for val in datas:
                
                view_mode=['tree', 'form']
                id = val.get('temp_id')
                model=self.model
                name = 'ofc'
                
#            links = ["javascript: test_link('%s');" % (model)]
#            'new ManyToOne(%s); return false;'" % (model)
#            links = urllib.quote_plus(link)
            
            value = []
            total = 0
            value = values.values()[0]
            
            for i in value:
                total = total+i
            
            val = []
            
            for j in value:
                val.append(round((j*100)/total))
                    
            colours = colors
            bg_colour ='#FFFFFF'            
            line_size = 60
            
            pie = "%s,%s,%s" % (70, 'red', 'blue')
        
            if( gradient ):
                pie += ",%s" %("true")
        
            if ( border_size > 0 ):
                if ( gradient ):
                    pie += ","
                pie += ",%s" %(border_size)
            
            tmp += '&pie=%s&\r\n' % pie
            
            tmp += '&values=%s&\r\n' % ','.join([str(v) for v in val])
            tmp += '&pie_labels=%s&\r\n' % ','.join([str(val) for val in label_x])
            tmp += '&links=%s&\r\n' % ','.join(links)
            tmp += '&colours=%s&\r\n' % ','.join(colours)        
            tmp += "&pie=%s%s, {font-size:%s;}" % (pie_label_size, ', #000000', '12px')
            tmp += '&bg_colour=%s&\r\n' % bg_colour
            
            tmp += '&tool_tip=%s&\r\n' % ( 'Label: #x_label#<br>Value: #val#' )
            
        elif kind == 'bar':
            
            tmp = ''
            temp_lbl = []
            set_data = []
            
            for i in label_x:
                temp_lbl.append(urllib.quote_plus(i))
            
            tmp += '&x_label_style=%s,%s,%s,%s&\r\n' % (10, '#000000', 2, 1)
            tmp += '&x_axis_steps%s&\r\n' % (1)
            tmp += '&x_labels=%s&\r\n' % ",".join(str(label) for label in temp_lbl)         
            
            mx = 10
            for i, x in enumerate(axis[1:]):
                title = x
                data = values[x]
#                link = dom
#                chart.set_data(data)
                bg_colour ='#FFFFFF'
#                chart.set_links(link)
                mx = max(mx, *data)
                
                if ( len( lines ) == 0):
                    tmp += "&bar="
                    
                if( len( lines ) > 0 ):
                    tmp += '&bar_%s=' % (len( lines )+1)
                        
                tmp += "%s,%s,%s,%s" % (80, colors[i], colors[i], title)
                tmp += "&\r\n"
                    
                lines.append( tmp )
            
                if( len( set_data ) == 0 ):
                    set_data.append( '&values=%s&\r\n' % ','.join([str(v) for v in data]) )
                else:
                    set_data.append( '&values_%s=%s&\r\n' % (len(set_data)+1, ','.join([str(v) for v in data])) )
                
                tmp += "".join(set_data)
            
                tmp += '&y_max=%s&\r\n' % mx
                tmp += '&bg_colour=%s&\r\n' % bg_colour
                
                #mx = math.floor(math.log10(mx)) * 100
                #chart.set_y_max(mx)
                #chart.y_label_steps(mx / 10)
                
        return tmp              
