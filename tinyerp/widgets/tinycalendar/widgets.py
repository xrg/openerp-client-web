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

import time
import datetime
import calendar

import cherrypy
import turbogears as tg

from tinyerp import rpc
from tinyerp import tools
from tinyerp.utils import TinyDict

from tinyerp.widgets import interface

from base import TinyCalendar

from utils import Day
from utils import Week
from utils import Month

class MiniCalendar(tg.widgets.CompoundWidget, interface.TinyWidget):
    template = 'tinyerp.widgets.tinycalendar.templates.mini'
    params = ['selected_day', 'month', 'forweek', 'highlight']
    
    month = None
    selected_day = None
    forweek = False
    highlight = True
        
    def __init__(self, selected_day, forweek=False, highlight=True):        
        self.month = Month(selected_day.year, selected_day.month)
        self.selected_day = selected_day
        self.forweek = forweek
        self.highlight = highlight
        
class GroupBox(tg.widgets.CompoundWidget, interface.TinyWidget):
    template = 'tinyerp.widgets.tinycalendar.templates.groups'
    params = ["colors", "color_values", "action", "title"]
        
    colors = {}
    color_values = []
    title = None
    action = None
        
    def __init__(self, colors, color_values, selected_day, title=None, mode='month'):
        self.colors = colors
        self.color_values = color_values
        self.action = "/calendar/get"
        self.title = title
        
        if mode == 'day':
            self.action = "%s/%s" %(self.action, selected_day.isoformat())            
        elif mode == 'week':
            self.action = "%s/%s/%s" %(self.action, selected_day.week[0].isoformat(), selected_day.week[-1].isoformat())
        else:
            self.action = "%s/%s/%s" %(self.action, selected_day.year, selected_day.month)        

class MonthCalendar(TinyCalendar):

    template = 'tinyerp.widgets.tinycalendar.templates.month'
    params = ['month', 'events', 'selected_day', 'calendar_fields']
    member_widgets = ['minical', 'groupbox', 'use_search']    

    month = None
    events = {}
    
    minical = None
    groupbox = None    

    def __init__(self, model, view, ids=None, domain=[], context={}, options=None):
        
        TinyCalendar.__init__(self, model, ids, view, domain, context, options)                
        
        y, m = time.localtime()[:2]
        if options:
            y = options.year
            m = options.month

        self.month = Month(y, m)
        self.events = self.get_events([d for d in self.month])
        
        if not self.selected_day:
            sd = Day.today()
            if sd.year == y and sd.month == m:
                self.selected_day = sd
            else:
                self.selected_day = Day(y, m, 1)

        if not (self.selected_day.year == y and self.selected_day.month == m):
            self.minical = MiniCalendar(Day(y, m, 1))
        else:
            self.minical = MiniCalendar(self.selected_day)
            
        self.groupbox = GroupBox(self.colors, self.color_values, self.selected_day, title=(self.color_field or None) and self.fields[self.color_field]['string'], mode='month')
            
            
class WeekCalendar(TinyCalendar):
    template = 'tinyerp.widgets.tinycalendar.templates.week'
    params = ['week', 'events', 'selected_day', 'calendar_fields']
    member_widgets = ['minical', 'groupbox', 'use_search']
    
    week = None
    events = {}
    
    minical = None
         
    def __init__(self, model, view, ids=None, domain=[], context={}, options=None):            
        TinyCalendar.__init__(self, model, ids, view, domain, context, options)

        y, m, d = time.localtime()[:3]
        if options:
            y, m, d = options.date1[:3]
                        
        self.week = Week(Day(y,m,d))
        
        self.events = self.get_events([d for d in self.week])        
        self.selected_day = self.selected_day or self.week[0]

        self.minical = MiniCalendar(self.week[0], True)
        self.groupbox = GroupBox(self.colors, self.color_values, self.week[0], title=(self.color_field or None) and self.fields[self.color_field]['string'], mode='week')

class DayCalendar(TinyCalendar):
    template = 'tinyerp.widgets.tinycalendar.templates.day'
    params = ['day', 'events', 'calendar_fields']
    member_widgets = ['minical', 'groupbox', 'use_search']
    
    day = None
    events = {}
    
    minical = None
         
    def __init__(self, model, view, ids=None, domain=[], context={}, options=None):            
        TinyCalendar.__init__(self, model, ids, view, domain, context, options)
        
        y, m, d = time.localtime()[:3]
        if options:
            y, m, d = options.date1[:3]
                     
        self.day = Day(y,m,d)

        self.events = self.get_events([self.day])        
        self.minical = MiniCalendar(self.day)
        self.groupbox = GroupBox(self.colors, self.color_values, self.day, title=(self.color_field or None) and self.fields[self.color_field]['string'], mode='day')
