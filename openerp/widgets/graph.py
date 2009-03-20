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

import os
import time
import random
import locale
import xml.dom.minidom
import urllib

import turbogears as tg

from openerp import rpc
from openerp import tools
from openerp import common
from openerp import cache

from interface import TinyCompoundWidget

DT_FORMAT = '%Y-%m-%d'
DHM_FORMAT = '%Y-%m-%d %H:%M:%S'
HM_FORMAT = '%H:%M:%S'

if not hasattr(locale, 'nl_langinfo'):
    locale.nl_langinfo = lambda *a: '%x'

if not hasattr(locale, 'D_FMT'):
    locale.D_FMT = None

class Graph(TinyCompoundWidget):

    template = "openerp.widgets.templates.graph"
    javascript = [tg.widgets.JSLink("openerp", "javascript/swfobject.js")]
                  
    params = ['chart_type', 'chart_name', 'model', 'view_id', 'ids', 'domain', 'context', 'width', 'height']
    
    def __init__(self, model, view_id=False, ids=[], domain=[], context={}, width='350px', height='350px'):

        self.model = model
        self.view_id = view_id
        self.ids = ids
        self.domain = domain
        self.context = context
        
        self.width = width
        self.height = height
        
        cxt = rpc.session.context.copy()
        cxt.update(context or {})
        
        view = cache.fields_view_get(model, view_id, 'graph', cxt)
        
        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]
        attrs = tools.node_attributes(root)

        self.string = attrs.get('string', '')
        self.chart_type = attrs.get('type', 'pie')
        self.chart_name = 'graph_%s' % (random.randint(0,10000)) 

        if self.chart_type == 'pie':
            self.width="100%"
            
        if ids is None:
            self.ids = rpc.RPCProxy(model).search(domain)

class GraphData(object):
    
    def __init__(self, model, view_id=False, ids=[], domain=[], context={}):

        ctx = {}
        ctx = rpc.session.context.copy()
        ctx.update(context)

        view = cache.fields_view_get(model, view_id, 'graph', ctx)
        fields = view['fields']
        
        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]
                
        attrs = tools.node_attributes(root)
        
        self.model = model
        self.string = attrs.get('string', 'Unknown')
        self.kind = attrs.get('type', '')
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
            
            if isinstance(value[axis[0]], (tuple, list)):
                res['id'] = value[axis[0]][0]
            else:
                res['id'] = value[axis[0]]
                
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
    
    def get_data(self):
        
        if self.values:
            res = self.get_graph_data()
            return res
        
        return dict(title=self.string)
    
    def get_graph_data(self):
        
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
        
        temp_dom = []        
        label_x = []
        total_ids = []
        domain = []
        
        for field in axis[1:]:
            
            for val in datas:
                key_ids = {}
                key_ids['id'] = val.get('id')
                key_ids['rec_id'] = val.get('rec_id')
                key_ids['prod_id'] = val[axis[0]]
                lbl = val[axis[0]]
                key = urllib.quote_plus(val[axis[0]].encode('utf-8'))
                info = data_axis.setdefault(key, {})
                
                keys[key] = 1
                label[lbl] = 1
                
                if field in info:
                    oper = operators[axis_data[field].get('operator', '+')]
                    info[field] = oper(info[field], val[field])
                else:
                    info[field] = val[field]
                    
                total_ids += [key_ids]
                
        keys = keys.keys()
        keys.sort()

        label = label.keys()
        label.sort()
        
        for l in label:
            x = 0
            for i in total_ids:
                if i.get('prod_id') == l and x == 0:
                    dd = i.get('id')
                    x += 1            
                    temp_dom.append(dd)
                    
            if(len(l) > 10):
                label_x.append(l.split('/')[-1])
            else:
                label_x.append(l)
        
        for d in temp_dom:
            
            for val in datas:
                rec = val.get('rec_id')            
            domain += [[(axis[0], '=', d), ('id', 'in', rec)]]
            
        values = {}
        for field in axis[1:]:
            values[field] = map(lambda x: data_axis[x][field], keys)
    
        return values, domain, self.model, label_x, axis
    
class BarChart(GraphData):
    
    def __init__(self, model, view_id=False, ids=[], domain=[], context={}):
        super(BarChart, self).__init__(model, view_id, ids, domain, context)
        
    def get_data(self):
        
        result = {}
        ctx =  rpc.session.context.copy()
        
        res = super(BarChart, self).get_data()
        
        if len(res) > 1:
            values = res[0]
            domain = res[1]
            model = res[2]
            label_x = res[3]
            axis = res[4]
        else:
            return res
        
        def minmx_ticks(values):
        
            yopts = {}
            mx = 0
            mn = 0
            tk = 2
            
            for i,j in enumerate(values):
                mx = max(mx, values[i])
                mn = min(mn, values[i])
            
            if mx != 0:
                if mx < 0:
                    mx = mx - (10 + mx % 10)
                else:
                    mx = mx + (10 - (mx % 10))  
            
            if mn != 0:
                if mn < 0:
                    mn = mn - (10 + mn % 10)
                else:
                    mn = mn + (10 - (mn % 10))

            
            total = abs(mx) + abs(mn)
            tk = round(total/5)
            
            while (tk > 10):
                tk = round(tk/2)
            
            yopts['y_max'] = mx;
            yopts['y_min'] = mn;
            yopts['y_steps'] = tk;
            
            return yopts;
        
        temp_lbl = []
        dataset = result.setdefault('dataset', [])
        ChartColors = ['#c4a000', '#ce5c00', '#8f5902', '#4e9a06', '#204a87', '#5c3566', '#a40000', '#babdb6', '#2e3436'];
        
        for i in label_x:
            lbl = {}
            lbl['text'] = i
            lbl['colour'] = "#432BAF" 
            temp_lbl.append(lbl)
        
        urls = []
        url = []            
        
        for i, x in enumerate(axis[1:]):
            for dom in domain:                    
                u = tg.url('/form/find', _terp_view_type='tree', _terp_view_mode="['tree', 'graph']", 
                       _terp_domain=ustr(dom), _terp_model=self.model, _terp_context=ustr(ctx))
            
                url.append(u)  # urllib.quote_plus(u))
            urls += [[url]]
        
        allvalues = []
        
        for i, x in enumerate(axis[1:]):
            datas = []
            data = values[x]
            
            for j, d in enumerate(data):
                dt = {}
                dt["on-click"]= "function(){onChartClick('" + url[j] + "')}"
                dt['top'] = d
                datas.append(dt)
                allvalues.append(d)
                
            dataset.append({"text": axis[i+1], 
                            "type": "bar_3d",
                            "colour": ChartColors[i+3], 
                            "values": datas,
                            "font-size": 10})
            
        yopts = minmx_ticks(allvalues)
                    
        result = {"y_axis": {"steps": yopts['y_steps'], "max": yopts['y_max'], "min": yopts['y_min'],
                             'stroke': 2},
                  "title": {"text": ""},
                  "elements": [i for i in dataset],
                  "bg_colour": "#FFFFFF",
                  "x_axis": {"colour": "#909090",
                             "stroke": 1, 
                             "tick-height": 5,
                             "grid-colour" : "#FFFFFF",
                             "steps": 1, "labels": { "rotate": "diagonal", "colour": "#ff0000", "labels": [l for l in temp_lbl]},
                             "3d": 3
                             }
                  }
        
        return result

    
class PieChart(GraphData):
    
    def __init__(self, model, view_id=False, ids=[], domain=[], context={}):
        super(PieChart, self).__init__(model, view_id, ids, domain, context)
    
    def get_data(self):
        
        result = {}
        ctx =  rpc.session.context.copy()
        
        res = super(PieChart, self).get_data()
        
        if len(res) > 1:
            values = res[0]
            domain = res[1]
            model = res[2]
            label_x = res[3]
            axis = res[4]
        else:
            return res
            
        ChartColors = ['#204a87', '#8f5902', '#4e9a06', '#5c3566', '#a40000', '#c4a000', '#ce5c00','#babdb6', '#2e3436'];
        
        dataset = result.setdefault('dataset', [])            
        value = values.values()[0]
       
        url = []
        
        for dom in domain:
            u = tg.url('/form/find', _terp_view_type='tree', _terp_view_mode="['tree', 'graph']", 
                       _terp_domain=ustr(dom), _terp_model=self.model, _terp_context=ustr(ctx))
            
            url.append(u)
        
        allvalues = []
        for i, x in enumerate(label_x):
            val = {}
            val['value'] = value[i]
            val['label'] = x
            val['on-click'] = "function(){onChartClick('" + url[i] + "')}"
            allvalues.append(val)
            
        for i, x in enumerate(label_x):
            dataset.append({'type': 'pie', 
                            "colours": [c for c in ChartColors], 
                            "border": 1,
                            "animate": "true", 
                            "label-colour": "#432BAF", 
                            "alpha": 0.30,
                            "gradient-fill": 'true',
                            "tip": "#label# (#percent#)",
                            "values": allvalues})
        
        result = {"elements": [d for d in dataset],
                  "bg_colour": "#FFFFFF"}

        return result
    
# vim: ts=4 sts=4 sw=4 si et

