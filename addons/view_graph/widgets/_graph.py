# -*- encoding: utf-8 -*-
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
import locale
import random
import re
import time
import urllib
import xml.dom.minidom

import simplejson
from openerp.utils import rpc, cache, node_attributes
from openerp.widgets import TinyWidget
from openobject.tools import url_plus
from openobject.widgets import JSSource, JSLink


DT_FORMAT = '%Y-%m-%d'
DHM_FORMAT = '%Y-%m-%d %H:%M:%S'
HM_FORMAT = '%H:%M:%S'

if not hasattr(locale, 'nl_langinfo'):
    locale.nl_langinfo = lambda *a: '%x'

if not hasattr(locale, 'D_FMT'):
    locale.D_FMT = None


COLOR_PALETTE = ['#75507b', '#3465a4', '#73d216', '#c17d11', '#edd400', '#fcaf3e', '#ef2929', '#ff00c9',
                 '#ad7fa8', '#729fcf', '#8ae234', '#e9b96e', '#fce94f', '#f57900', '#cc0000', '#d400a8',
                 '#ff8e00', '#ff0000', '#b0008c', '#9000ff', '#0078ff', '#00ff00', '#e6ff00', '#ffff00',
                 '#905000', '#9b0000', '#840067', '#9abe00', '#ffc900', '#510090', '#0000c9', '#009b00']

_colorline = ['#%02x%02x%02x' % (25+((r+10)%11)*23,5+((g+1)%11)*20,25+((b+4)%11)*23) for r in range(11) for g in range(11) for b in range(11) ]
def choice_colors(n):
    if n > len(COLOR_PALETTE):
        return _colorline[0:-1:len(_colorline)/(n+1)]
    elif n:
        return COLOR_PALETTE[:n]
    return []


class Graph(TinyWidget):

    template = "/view_graph/widgets/templates/graph.mako"
    javascript = [
        JSLink("view_graph", "javascript/swfobject.js"),
        JSLink("view_graph", "javascript/graph.js")]

    params = ['width', 'height', 'data']
    width = 360
    height = 300

    def __init__(self, model, view=False, view_id=False, ids=[], domain=[], context={},view_mode=[], width=360, height=300):

        name = 'graph_%s' % (random.randint(0,10000))
        super(Graph, self).__init__(name=name, model=model, width=width, height=height)

        ctx = rpc.session.context.copy()
        ctx.update(context or {})
        view = view or cache.fields_view_get(model, view_id, 'graph', ctx)

        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]
        attrs = node_attributes(root)

        self.string = attrs.get('string')

        chart_type = attrs.get('type', 'pie')

        self.ids = ids
        if ids is None:
            self.ids = rpc.RPCProxy(model).search(domain, 0, 0, 0, ctx)
        self.count = rpc.RPCProxy(model).search_count(domain, ctx)
        if chart_type == "bar":
            self.data = BarChart(model, view, view_id, ids, domain, view_mode, context)
        else:
            self.data = PieChart(model, view, view_id, ids, domain, view_mode, context)

        self.data = simplejson.dumps(self.data.get_data())

class GraphData(object):

    def __init__(self, model, view=False, view_id=False, ids=[], domain=[], view_mode=[], context={}):

        ctx = {}
        ctx = rpc.session.context.copy()
        ctx.update(context)

        view = view or cache.fields_view_get(model, view_id, 'graph', ctx)
        fields = view['fields']

        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]

        attrs = node_attributes(root)

        self.view_mode = view_mode
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
                if fields[x]['type'] in ('many2one', 'char','time','text'):
                    res[x] = value[x]
                    if isinstance(res[x], (list, tuple)):
                        res[x] = res[x][-1]
                    res[x] = ustr(res[x])
                elif fields[x]['type'] in 'selection':
                    for i in fields[x]['selection']:
                        if value[x] in i:
                            res[x] = i[1]
                elif fields[x]['type'] == 'date':
                    if value[x]:
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
                        res[x] = time.strftime(locale.nl_langinfo(locale.D_FMT).replace('%y', '%Y'), date)
                    else:
                        res[x] = ''
                elif fields[x]['type'] == 'datetime':
                    if value[x]:
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
                        res[x] = ''
                else:
                    res[x] = float(value[x])

            if axis and isinstance(value[axis[0]], (tuple, list)):
                res['id'] = value[axis[0]][0]
            elif axis:
                res['id'] = value[axis[0]]
            else:
                res['id'] = False

            res['rec_id'] = rec_ids

            self.values.append(res)

        self.axis = axis
        self.axis_data = axis_data
        self.axis_group_field = axis_group

    def parse(self, root, fields):

        attrs = node_attributes(root)

        axis = []
        axis_data = {}
        axis_group = {}

        for node in root.childNodes:
            attrs = node_attributes(node)
            if node.localName == 'field':
                name = attrs['name']
                fields[name].update(attrs) # Update fields ...

                attrs['string'] = fields[name]['string']

                axis.append(ustr(name))
                axis_data[ustr(name)] =  attrs

        for i in axis_data:
            axis_data[i]['string'] = fields[i]['string']
            if axis_data[i].get('group', False):
                axis_group[i]=1
                axis.remove(i)

        return axis, axis_data, axis_group

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

        axis_group = {}
        data_all = {}
        data_ax = []

        temp_dom = []
        label_x = []
        total_ids = []
        domain = []

        for field in axis[1:]:
            data_all = {}
            for val in datas:
                group_eval = ','.join(map(lambda x: val[x], self.axis_group_field.keys()))
                axis_group[group_eval] = 1

                key_ids = {}
                key_ids['id'] = val.get('id')
                key_ids['rec_id'] = val.get('rec_id')
                key_ids['prod_id'] = val[axis[0]]
                lbl = val[axis[0]]
                
                val[axis[0]] = ustr(val[axis[0]])
                key_value = val[axis[0]]
                key = urllib.quote_plus(ustr(key_value).encode('utf-8'))
                info = data_axis.setdefault(key, {})

                data_all.setdefault(key_value, {})

                keys[key] = 1
                label[lbl] = 1

                if field in info:
                    oper = operators[axis_data[field].get('operator', '+')]
                    info[field] = oper(info[field], val[field])
                else:
                    info[field] = val[field]

                if group_eval in data_all[val[axis[0]]]:
                     oper = operators[axis_data[field].get('operator', '+')]
                     data_all[val[axis[0]]][group_eval] = oper(data_all[val[axis[0]]][group_eval], val[field])
                else:
                    data_all[val[axis[0]]][group_eval] = val[field]

                total_ids += [key_ids]
            data_ax.append(data_all)
        axis_group = axis_group.keys()
        axis_group.sort()
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

            if not isinstance(l, basestring):
                l = ustr(l)

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

        n = len(axis)-1
        stack_list = []
        stack_id_list = []
        val = []
        grp_value = []

        if len(axis_group) > 1 and kind == 'bar':

            group_field = self.axis_group_field.keys()[0]
            new_keys = []
            for k in keys:
                k = urllib.unquote_plus(k)
                k = k.decode('utf-8')
                new_keys += [k]

            keys = new_keys
            for i in range(n):

                data = data_ax[i]
                group_data = {}

                for key in keys:
                    group_data[key] = {}
                    for dt in data:
                        for d in data[dt]:
                            ids = []
                            for dts in datas:
                                if dt == dts[axis[0]] and d == dts[group_field] and dt == key:
                                    ids += [dts['temp_id']]
                                    group_data[key][d] = str(data[dt][d]) + '/' + str(ids)

                for y in range(len(axis_group)):
                    for field in axis[1:]:
                        values[field] = [data[x].get(axis_group[y], 0.0) for x in new_keys]
                for x in new_keys:
                    for field in axis[1:]:
                        v = [data[x].get(axis_group[y], 0.0) for y in range(len(axis_group))]
                        grp_v = [group_data[x].get(axis_group[y], '0.0') for y in range(len(axis_group))]
                        val.append(v)
                        grp_value.append(grp_v)
                stack_list += val
                stack_id_list += grp_value

#        IF VALUES ARE ALL 0...
#        if stack_list and len(stack_list) > 0:
#            if stack_list[0] and len(stack_list[0]) > 0:
#                min_stack_val = min(stack_list[0])
#                max_stack_val = max(stack_list[0])
#
#                if min_stack_val == max_stack_val == 0 or min_stack_val == max_stack_val == 0.0:
#                    return dict(title=self.string)

        return values, domain, self.model, label_x, axis, axis_group, stack_list, keys, axis_data, stack_id_list

class BarChart(GraphData):

    def __init__(self, model, view=False, view_id=False, ids=[], domain=[], view_mode=[], context={}):
        super(BarChart, self).__init__(model, view, view_id, ids, domain, view_mode, context)
        self.context = context

    def get_data(self):

        result = {}
        ctx =  rpc.session.context.copy()
        ctx.update(self.context)
        res = super(BarChart, self).get_graph_data()

        if len(res) > 1:
            values = res[0]
            domain = res[1]
            model = res[2]
            label_x = res[3]
            axis = res[4]
            axis_group = res[5]
            stack_list = res[6]
            stack_labels = res[7]
            axis_data = res[8]
            stack_id_list = res[9]
        else:
            return res

        def minmx_ticks(values):

            x_data = []

            for st in stack_list:
                range = 0
                for s in st:
                    range = range + s
                x_data += [range]

            yopts = {}
            mx = 0
            mn = 0
            tk = 2

            if values:
                values.sort()
                if x_data:
                    x_data.sort()
                    mx = x_data[-1]
                else:
                    mn = 0
                    mx = values[-1]

            if mx != 0:
                if mx < 0:
                    mx = mx - (10 + mx % 10)
                else:
                    mx = mx + (10 - (mx % 10))

            total = mx + mn
            tk = round(total/10)

            yopts['y_max'] = mx;
            yopts['y_min'] = mn;
            yopts['y_steps'] = tk;

            return yopts;

        temp_lbl = []
        dataset = result.setdefault('dataset', [])

        for i in label_x:
            lbl = {}
            i = re.sub(u'[êéèë]', 'e', i)
            i = re.sub(u'[ïî]', 'i', i)
            i = re.sub(u'[àâáâãä]', 'a', i)
            i = re.sub(u'[ç]', 'c', i)
            i = re.sub(u'[òóôõö]', 'o', i)
            i = re.sub(u'[ýÿ]', 'y', i)
            i = re.sub(u'[ñ]', 'n', i)
            i = re.sub(u'[ÁÂÃÄ]', 'A', i)
            i = re.sub(u'[ÈÉÊË]', 'E', i)
            i = re.sub(u'[ÌÍÎÏ]', 'I', i)
            i = re.sub(u'[ÒÓÔÕÖ]', 'O', i)
            i = re.sub(u'[ÙÚÛÜ]', 'U', i)
            i = re.sub(u'[Ý]', 'Y', i)
            i = re.sub(u'[Ñ]', 'N', i)

            lbl['text'] = i
            lbl['colour'] = "#432BAF"
            temp_lbl.append(lbl)

        url = []

        for x in axis[1:]:
            if len(axis_group) > 1:
                for st in stack_id_list:
                    for s in st:
                        if s.find('/') != -1:
                            ids = s.split('/')[1]
                            ids = eval(ids)
                            dom = [('id', 'in', ids)]
                            u = url_plus('/openerp/form/find', _terp_view_type='tree', _terp_view_mode=ustr(self.view_mode),
                               _terp_domain=ustr(dom), _terp_model=self.model, _terp_context=ustr(ctx))

                            url.append(u)

            else:
                for dom in domain:
                    u = url_plus('/openerp/form/find', _terp_view_type='tree', _terp_view_mode=ustr(self.view_mode),
                           _terp_domain=ustr(dom), _terp_model=self.model, _terp_context=ustr(ctx))

                    url.append(u)

        allvalues = []

        ChartColors = choice_colors(len(axis))

        for i, x in enumerate(axis[1:]):
            data = values[x]

            for j, d in enumerate(data):
                allvalues.append(d)

        yopts = minmx_ticks(allvalues)

        y_grid_color = True

        if yopts['y_steps'] == 0.0:
            yopts['y_steps'] = 1
            yopts['y_max'] = 9
            yopts['y_min'] = 0
            y_grid_color = False

        if y_grid_color:
            axis_y = {"steps": yopts['y_steps'], "max": yopts['y_max'], "min": yopts['y_min'],
                      "stroke": 2 , "grid-colour": "#F0EEEE"}
        else:
            axis_y = {"steps": yopts['y_steps'], "max": yopts['y_max'], "min": yopts['y_min'],
                      'stroke': 2 , "grid-colour": "#F0EEEE"}

        if len(axis_group) > 1:
            ChartColors = choice_colors(len(axis_group))
            all_keys = []
            for i, x in enumerate(axis_group):
                data = {}
                data['text'] = x
                data['colour'] = ChartColors[i]
                data['font-size'] = 12
                all_keys.append(data)

            stack_val = []
            cnt = 0
            for j, stk in enumerate(stack_list):
                sval = []
                for x, s in enumerate(stk):
                    stack = {}
                    stack['val'] = s
                    if s != 0.0 and not ctx.get('report_id', False) and url:
                        stack["on-click"]= "function(){onChartClick('" + url[cnt] + "')}"
                        cnt += 1
                    stack['tip'] = s
                    sval.append(stack)
                stack_val.append(sval)

            result = { "elements": [{"type": "bar_stack",
                                     "colours": ChartColors,
                                     "values": [s for s in stack_val],
                                     "keys": [key for key in all_keys]}],
                        "x_axis": {"colour": "#909090",
                                   "labels": { "labels": [ lbl for lbl in stack_labels ], "rotate": "diagonal", "colour": "#ff0000"},
                                   "3d": 3, "grid-colour": "#F0EEEE"},
                        "y_axis": axis_y,
                        "bg_colour": "#F8F8F8",
                        "tooltip": {"mouse": 2 }}

        else:
            for i, x in enumerate(axis[1:]):
                datas = []
                data = values[x]

                for j, d in enumerate(data):
                    dt = {}
                    if not ctx.get('report_id', False):
                        dt["on-click"]= "function(){onChartClick('" + url[j] + "')}"
                    dt['top'] = d
                    datas.append(dt)
                    allvalues.append(d)

                dataset.append({"text": axis_data[x]['string'],
                                "type": "bar_3d",
                                "colour": ChartColors[i],
                                "values": datas,
                            "font-size": 10})

            result = {"y_axis": axis_y,
                      "title": {"text": ""},
                      "elements": [i for i in dataset],
                      "bg_colour": "#F8F8F8",
                      "x_axis": {"colour": "#909090",
                                 "stroke": 1,
                                 "tick-height": 5,
                                 "steps": 1, "labels": { "rotate": "diagonal", "colour": "#ff0000", "labels": [l for l in temp_lbl]},
                                 "3d": 3,
                                 "grid-colour": "#F0EEEE"
                                 }
                      }
        return result


class PieChart(GraphData):

    def __init__(self, model, view=False, view_id=False, ids=[], domain=[], view_mode=[], context={}):
        super(PieChart, self).__init__(model, view, view_id, ids, domain, view_mode, context)

    def get_data(self):

        result = {}
        ctx =  rpc.session.context.copy()

        res = super(PieChart, self).get_graph_data()

        if len(res) > 1:
            values = res[0]
            domain = res[1]
            model = res[2]
            label_x = res[3]
            axis = res[4]
        else:
            return res

        dataset = result.setdefault('dataset', [])
        value = values.values()[0]

        url = []
        for dom in domain:
            u = url_plus('/openerp/form/find', _terp_view_type='tree', _terp_view_mode=ustr(self.view_mode),
                       _terp_domain=ustr(dom), _terp_model=self.model, _terp_context=ustr(ctx))

            url.append(u)

        allvalues = []
        per = []
        total_val = 0
        for i, x in enumerate(label_x):
            total_val += value[i]

        for i, x in enumerate(label_x):
            val = {}
            val['value'] = value[i]
            val['text'] = x
            val['label'] = x
            if not ctx.get('report_id', False):
                val['on-click'] = "function(){onChartClick('" + url[i] + "')}"

            if total_val <> 0.0:
                field_key = (100 * value[i])/total_val
                field_key = '%.2f' % (field_key)
                val["tip"] = x + ' (' + field_key + ' %)'
            else:
                val["tip"] = x

            allvalues.append(val)

        ChartColors = choice_colors(len(allvalues))

        dataset.append({'type': 'pie',
                        "colours": ChartColors,
                        "animate": "true",
                        "gradient-fill": 'true',
                        "no-labels": 'true',
                        "values": allvalues})

        result = {"legend": {"bg_colour": "#f8f8f8",
                             "border": 'true',
                             "position": "top",
                             "shadow": 'true',
                             "visible": 'true'
                             },
                  "elements": [d for d in dataset],
                  "bg_colour": "#F8F8F8"}

        return result

# vim: ts=4 sts=4 sw=4 si et
