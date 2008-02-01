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

import math
import time
import datetime
import xml.dom.minidom

import cherrypy
import turbogears as tg

from tinyerp import rpc
from tinyerp import tools
from tinyerp import format
from tinyerp.utils import TinyDict

from tinyerp.widgets import interface

from utils import Day
from utils import parse_datetime

from tinyerp.tinygraph import choice_colors

class TinyEvent(tg.widgets.Widget, interface.TinyWidget):
    
    template = """<div xmlns:py="http://purl.org/kid/ns#" class="calEvent" style="background-color: ${color}"
    starts="${str(starts)}" ends="${str(ends)}" record_id="${record_id}" py:content="title" title="${description}">
    </div>
    """

    params = ['starts', 'ends', 'title', 'description', 'color', 'record_id']

    starts = None
    ends = None
    dayspan = 0
    color = None
    
    title = ''
    description = ''

    record = {}
    record_id = False
    
    def __init__(self, record, starts, ends, title='', description='', dayspan=0, color=None):
        
        self.record = record
        self.record_id = record['id']
        
        if starts and ends:

            self.starts = (starts or None) and datetime.datetime(*starts[:6])
            self.ends = (ends or None) and datetime.datetime(*ends[:6])

        self.dayspan = dayspan
                    
        self.title = title
        self.description = description
        self.color = color

class TinyCalendar(interface.TinyCompoundWidget):
    
    date_start = None
    date_delay = None
    date_stop = None
    color_field = None
    day_length = 8

    info_fields = []    
    fields = []
    
    colors = {}
    color_values = []
    use_search = False

    events = {}
    
    selected_day = None
    calendar_fields = {}
    
    date_format = '%Y-%m-%d'
    
    css = [tg.widgets.CSSLink('tinyerp', 'tinycalendar/css/calendar.css')]
    javascript = [tg.widgets.JSLink('tinyerp', 'tinycalendar/javascript/New.js'),
                  tg.widgets.JSLink('tinyerp', 'tinycalendar/javascript/Visual.js'),
                  tg.widgets.JSLink('tinyerp', 'tinycalendar/javascript/DragAndDrop.js'),
                  tg.widgets.JSLink('tinyerp', 'tinycalendar/javascript/Resizable.js'),
                  tg.widgets.JSLink('tinyerp', 'tinycalendar/javascript/calendar_date.js'),
                  tg.widgets.JSLink('tinyerp', 'tinycalendar/javascript/calendar_utils.js'),
                  tg.widgets.JSLink('tinyerp', 'tinycalendar/javascript/calendar_box.js'),
                  tg.widgets.JSLink('tinyerp', 'tinycalendar/javascript/calendar_month.js'),
                  tg.widgets.JSLink('tinyerp', 'tinycalendar/javascript/calendar_week.js')]

    def __init__(self, model, ids, view, domain=[], context={}, options=None):

        self.ids = ids
        self.model = model        
        self.domain = domain or []
        self.context = context or {}
        self.options = options
                
        self.date_format = format.get_datetime_format('date')                
        self.use_search = (options or None) and options.use_search 
        
        try:            
            dt = parse_datetime(options.selected_day)
            self.selected_day = Day(dt.year, dt.month, dt.day)
        except:
            pass

        proxy = rpc.RPCProxy(model)

        view_id = view.get('view_id', False)

        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]
        attrs = tools.node_attributes(root)
        
        self.string = attrs.get('string', '')
        self.date_start = attrs.get('date_start') 
        self.date_delay = attrs.get('date_delay')
        self.date_stop = attrs.get('date_stop')
        self.color_field = attrs.get('color')
        self.day_length = int(attrs.get('day_length', 8))
        
        self.info_fields = self.parse(root, view['fields'])
        
        fields = view['fields']
        fields = fields.keys() + [self.date_start, self.date_stop, self.date_delay, self.color_field]

        fields = list(set([x for x in fields if x]))

        self.fields = proxy.fields_get(fields)
        
        self.colors = {}
        self.color_values = []
        
        if self.color_field and options and options.colors:
            self.colors = options.colors
            
        if self.color_field and options and options.color_values:
            self.color_values = options.color_values
            
        self.calendar_fields['date_start'] = dict(name=self.date_start, 
                                                  kind=self.fields[self.date_start]['type'])
        
        if self.date_delay:
            self.calendar_fields['date_delay'] = dict(name=self.date_delay, 
                                                      kind=self.fields[self.date_delay]['type'])
            
        if self.date_stop:
            self.calendar_fields['date_stop'] = dict(name=self.date_stop, 
                                                         kind=self.fields[self.date_stop]['type'])
            
        self.calendar_fields['day_length'] = self.day_length

    def parse(self, root, fields):
        
        info_fields = []
        attrs = tools.node_attributes(root)        

        for node in root.childNodes:
            attrs = tools.node_attributes(node)
            
            if node.localName == 'field':
                info_fields += [attrs['name']]

        return info_fields
   
    def convert(self, event):
        
        fields = [x for x in [self.date_start, self.date_stop] if x]
        
        for fld in fields:
            typ = self.fields[fld]['type']
            fmt = format.DT_SERVER_FORMATS[typ]

            if event[fld] and fmt:
                event[fld] = time.strptime(event[fld], fmt)
            
            # default start time is 9:00 AM
            if typ == 'date' and fld == self.date_start:
                ds = list(event[fld])
                ds[3] = 9
                event[fld] = tuple(ds)
   
    def get_events(self, days):
                    
        proxy = rpc.RPCProxy(self.model)
        
        #XXX: how to get events not falling between the given day range but spans the range?            
        #domain = self.domain + [(self.date_start, '>', days[0].prev().isoformat()), 
        #                        (self.date_start, '<', days[-1].next().isoformat())]
        
        first = days[0].month2.prev()[0] #HACK: add prev month
        domain = self.domain + [(self.date_start, '>', first.isoformat()), 
                                (self.date_start, '<', days[-1].next().isoformat())]
               
        if self.color_values: 
            domain += [(self.color_field, "in", self.color_values)]
            
        if self.options and self.options.use_search:
            domain += self.options.search_domain
            
        ctx = rpc.session.context.copy()
        ctx.update(self.context)

        ids = proxy.search(domain, 0, 0, 0, ctx)
        result = proxy.read(ids, self.fields.keys(), ctx)
        
        if self.color_field:
            
            for evt in result:   
                key = evt[self.color_field]
                name = key
                value = key
                
                if isinstance(key, tuple): #M2O 
                    value, name = key

                self.colors[key] = (name, value, None)

            colors = choice_colors(len(self.colors))
            for i, (key, value) in enumerate(self.colors.items()):
                self.colors[key] = (value[0], value[1], colors[i])
        
        events = []

        for evt in result:
            self.convert(evt)
            events += [self.get_event_widget(evt)]
        
        # filter out the events which are not in the range
        result = []
        for e in events:
            if e.dayspan > 0 and days[0] - e.dayspan < e.starts:
                result += [e]
            if e.dayspan == 0 and days[0] <= e.starts:
                result += [e]
        
        return result
    
    def get_event_widget(self, event):

        title = ''       # the title
        description = [] # the description
        starts = None    # the starting time (datetime)
        ends = None      # the end time (datetime)
        
        if self.info_fields:
            
            f = self.info_fields[0]
            s = event[f]
            
            if isinstance(s, (tuple, list)): s = s[-1]
            
            title = ustr(s)
        
            for f in self.info_fields[1:]:
                s = event[f]
                if isinstance(s, (tuple, list)): s = s[-1]
            
                description += [ustr(s)]

        starts = event.get(self.date_start)
        ends = event.get(self.date_delay) or 1.0
        span = 0
        
        if starts and ends:
            
            n = 0
            h = ends
            
            if ends == self.day_length: span = 1
            
            if ends > self.day_length:
                n = ends / self.day_length
                h = ends % self.day_length
            
                n = int(math.floor(n))
            
                if n > 0: span = n + 1
            
            ends = time.localtime(time.mktime(starts) + (h * 60 * 60) + (n * 24 * 60 * 60))
        
        if starts and self.date_stop:
            
            ends = event.get(self.date_stop)
            if not ends:
                ends = time.localtime(time.mktime(starts) + 60 * 60)
                
            tds = time.mktime(starts)
            tde = time.mktime(ends)
            
            if tds >= tde:
                tde = tds + 60 * 60
                ends = time.localtime(tde)
            
            n = (tde - tds) / (60 * 60)
            
            if n > self.day_length:
                span = math.floor(n / 24)

        starts = format.format_datetime(starts, "datetime", True)
        ends = format.format_datetime(ends, "datetime", True)
        
        color_key = event.get(self.color_field) 
        color = self.colors.get(color_key)

        title = title.strip()
        description = ', '.join(description).strip()
        
        return TinyEvent(event, starts, ends, title, description, dayspan=span, color=(color or None) and color[-1])       
