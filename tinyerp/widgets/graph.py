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
import random
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

    template = "tinyerp.widgets.templates.graph"

    javascript = [tg.widgets.JSLink("tinyerp", "javascript/swfobject.js"),
                  tg.widgets.JSLink("tinyerp", "javascript/charts.js")]
    
    params = ['chart_type', 'chart_name', 'model', 'view_id', 'ids', 'domain', 'context', 'width', 'height']
    
    def __init__(self, model, view_id=False, ids=[], domain=[], context={}, width='100%', height='350px'):

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
        self.chart_type = attrs.get('type', 'pie')
        self.chart_name = 'graph_%s' % (random.randint(0,10000)) 

        if ids is None:
            self.ids = rpc.RPCProxy(model).search(domain)
            
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
        
    def get_pie_data(self):
        
        kind = 'pie'
        result = self.get_graph_data(kind)
        
        return result
        
    def get_bar_data(self):
        
        kind = 'bar'
        result = self.get_graph_data(kind)
        
        return result

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
    
    def get_graph_data(self, kind):
        
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
        temp_dom = {}
        
        label_x = []
        total_ids = []
        domain = []
        
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
                temp_dom[dm] = 1
                
        keys = keys.keys()
        keys.sort()
        
        label = label.keys()
        label.sort()
        
        temp_dom = temp_dom.keys()
        temp_dom.sort()
        
        for field in axis[1:]:
            for d in temp_dom:
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
    
        result = {}
        
        if kind == 'pie':     
            total = 0
            result['title'] = self.string
            dataset = result.setdefault('dataset', [])
            
            value = values.values()[0]
            for v in value:
                total = total+v
            
            val = []
            
            for j in value:
                val.append(round((j*100)/total))
            
            legend = [axis_data[x]['string'] for x in axis[1:]]
            
            for i, x in enumerate(label_x):
                dataset.append({'legend': [x], 'value': val[i]})
            
        elif kind == 'bar':
            
            result['title'] = self.string
            dataset = result.setdefault('dataset', [])
                        
            temp_lbl = []
            
            legend = [axis_data[x]['string'] for x in axis[1:]]
            
            for i in label_x:
                temp_lbl.append(urllib.quote_plus(i))
                            
            result['x_labels'] = temp_lbl
            result['y_legend'] = ''
            
            for i, x in enumerate(axis[1:]):
                data = values[x]
                
                dataset.append({'legend': legend[i], 'values': data})
        
        return result  
