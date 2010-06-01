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

import time
import datetime
import calendar
import xml.dom.minidom

import cherrypy

from openobject.widgets import JSLink, CSSLink

from openerp.utils import rpc
from openerp.utils import TinyDict
from openerp.utils import node_attributes

from openerp.widgets import TinyWidget

from _base import ICalendar
from _base import TinyCalendar

from utils import Day
from utils import Week
from utils import Month
from utils import Year

class MiniCalendar(TinyWidget):
    template = 'templates/mini.mako'
    params = ['selected_day', 'month', 'forweek', 'highlight']

    month = None
    selected_day = None
    forweek = False
    highlight = True

    def __init__(self, selected_day, forweek=False, highlight=True):

        super(MiniCalendar, self).__init__()

        self.month = Month(selected_day.year, selected_day.month)
        self.selected_day = selected_day
        self.forweek = forweek
        self.highlight = highlight

class GroupBox(TinyWidget):
    template = 'templates/groups.mako'
    params = ["colors", "color_values", "title"]

    colors = {}
    color_values = []
    title = None
    action = None

    def __init__(self, colors, color_values, selected_day, title=None, mode='month'):
        super(GroupBox, self).__init__()
        self.colors = colors
        self.color_values = color_values
        self.title = title

def get_calendar(model, view, ids=None, domain=[], context={}, options=None):

    mode = (options or None) and options.mode
    if not mode:
        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        attrs = node_attributes(dom.childNodes[0])
        mode = attrs.get('mode')

    if mode == 'day':
        return DayCalendar(model, view, ids, domain, context, options)

    if mode == 'week':
        return WeekCalendar(model, view, ids, domain, context, options)

    return MonthCalendar(model, view, ids, domain, context, options)

def _get_selection_day(day, selected, mode):
    selected = selected or Day.today()

    if mode == 'day':
        return day

    if mode == 'week':
        return Week(day)[selected.weekday()]

    month = day.month2
    d = selected.day

    if d > month.range[-1]:
        d = month.range[-1]

    return Day(day.year, day.month, d)

class MonthCalendar(TinyCalendar):

    template = 'templates/month.mako'
    params = ['month', 'events', 'selected_day', 'calendar_fields', 'date_format']
    member_widgets = ['minical', 'groupbox']

    month = None
    events = {}

    def __init__(self, model, view, ids=None, domain=[], context={}, options=None):

        TinyCalendar.__init__(self, model, ids, view, domain, context, options)

        y, m = time.localtime()[:2]
        if options:
            y = options.year
            m = options.month

        self.month = Month(y, m)
        self.events = self.get_events(self.month.days)

        self.selected_day = _get_selection_day(Day(y, m, 1), self.selected_day, 'month')

        self.minical = MiniCalendar(self.selected_day)
        self.groupbox = GroupBox(self.colors, self.color_values, self.selected_day,
                title=(self.color_field or None) and self.fields[self.color_field]['string'],
                mode='month')


class WeekCalendar(TinyCalendar):
    template = 'templates/week.mako'
    params = ['week', 'events', 'selected_day', 'calendar_fields', 'date_format']
    member_widgets = ['minical', 'groupbox']

    week = None
    events = {}

    minical = None

    def __init__(self, model, view, ids=None, domain=[], context={}, options=None):
        TinyCalendar.__init__(self, model, ids, view, domain, context, options)

        y, m, d = time.localtime()[:3]
        if options:
            y, m, d = options.date1[:3]

        self.week = Week(Day(y, m, d))
        self.events = self.get_events(self.week.days)

        self.selected_day = _get_selection_day(Day(y, m, d), self.selected_day, 'week')

        self.minical = MiniCalendar(self.week[0], True)
        self.groupbox = GroupBox(self.colors, self.color_values, self.week[0],
                title=(self.color_field or None) and self.fields[self.color_field]['string'],
                mode='week')


class DayCalendar(TinyCalendar):
    template = 'templates/day.mako'
    params = ['day', 'events', 'calendar_fields', 'date_format']
    member_widgets = ['minical', 'groupbox']

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
        self.groupbox = GroupBox(self.colors, self.color_values, self.day,
                title=(self.color_field or None) and self.fields[self.color_field]['string'],
                mode='day')


class GanttCalendar(ICalendar):

    template = 'templates/gantt.mako'

    params = ['title', 'level', 'groups', 'days', 'events', 'calendar_fields', 'date_format',
              'selected_day', 'mode', 'headers', 'subheaders', 'model', 'ids']
    member_widgets = ['groupbox']

    level = None
    groups = None
    title = None
    days = None
    headers = None
    subheaders = None
    mode = 'week'

    css = [CSSLink("view_calendar", 'css/calendar.css'),
           CSSLink("view_calendar", 'css/calendar_gantt.css')]
    javascript = [JSLink("view_calendar", 'javascript/calendar_date.js'),
                  JSLink("view_calendar", 'javascript/calendar_utils.js'),
                  JSLink("view_calendar", 'javascript/calendar_box.js'),
                  JSLink("view_calendar", 'javascript/calendar_month.js'),
                  JSLink("view_calendar", 'javascript/calendar_week.js'),
                  JSLink("view_calendar", 'javascript/calendar_gantt.js')]

    def __init__(self, model, ids, view, domain=[], context={}, options=None):

        self.level = None
        self.groups = []
        self.days = []
        self.headers = []

        super(GanttCalendar, self).__init__(model, ids, view, domain, context, options)

        y, m, d = time.localtime()[:3]
        if options:
            y, m, d = options.date1[:3]

        day = Day(y, m, d)

        if self.mode == 'day':
            self.days = [day]
            self.title = ustr(day)
            self.selected_day = day

            self.headers = [(48, ustr(day))]
            self.subheaders = [time.strftime('%I %P', (y, m, d, i, 0, 0, 1, 1, 0)) for i in range(24)]

        elif self.mode == '3days':
            dp = day - 1
            dn = day + 1
            self.days = [dp, day, dn]
            self.title = u"%s, %s, %s" % (ustr(dp), ustr(day), ustr(dn))
            self.selected_day = day

            self.headers = [(24, ustr(dp)), (24, ustr(day)), (24, ustr(dn))]
            self.subheaders = []
            for x in self.headers:
                self.subheaders += [time.strftime('%I %P', (y, 1, 1, i, 0, 0, 1, 1, 0)) for i in range(0, 24, 6)]

        elif self.mode == 'week':
            self.days = [d for d in Week(day)]
            self.title = _("%s, Week %s") % (y, day.strftime("%W"))
            self.selected_day = _get_selection_day(day, self.selected_day, 'week')
            self.headers = [(12, u"%s %s" % (d.month2.name, d.day)) for d in self.days]
            self.subheaders = []
            for x in self.days:
                self.subheaders += [time.strftime('%I %P', (y, 1, 1, i, 0, 0, 1, 1, 0)) for i in [0, 23]]

        elif self.mode == '3weeks':
            w = Week(day)
            wp = w - 1
            wn = w + 1
            self.days = wp.days + w.days + wn.days
            self.title = _(u"%s - %s") % (ustr(self.days[0]), ustr(self.days[-1]))
            self.selected_day = _get_selection_day(day, self.selected_day, 'week')
            self.headers = [(7, _("Week %s") % w1[0].strftime('%W')) for w1 in [wp, w, wn]]
            self.subheaders = []
            self.subheaders += [x.strftime('%a %d') for x in wp]
            self.subheaders += [x.strftime('%a %d') for x in w]
            self.subheaders += [x.strftime('%a %d') for x in wn]

        elif self.mode == '3months':
            q = 1 + (m - 1) / 3

            mn = Month(y, q * 3)
            mt = mn.prev()
            mp = mt.prev()

            days = []
            days += [d for d in mp if d.year == mp.year and d.month == mp.month]
            days += [d for d in mt if d.year == mt.year and d.month == mt.month]
            days += [d for d in mn if d.year == mn.year and d.month == mn.month]

            self.days = days
            self.title = _("%s, Qtr %s") % (y, q)
            self.selected_day = _get_selection_day(day, self.selected_day, '3months')

            headers = []
            headers += [w for w in mp.weeks]
            headers += [w for w in mt.weeks]
            headers += [w for w in mn.weeks]

            self.headers = [(mp.range[-1], ustr(mp)), (mt.range[-1], ustr(mt)), (mn.range[-1], ustr(mn))]
            self.subheaders = []
            for x in headers:
                x = _("Week %s") % x[0].strftime('%W')
                if x not in self.subheaders:
                    self.subheaders += [x]

        elif self.mode == 'year':
            yr = Year(y)

            self.days = yr.days
            self.title = u"Year %s" % (y)
            self.selected_day = _get_selection_day(day, self.selected_day, 'year')
            self.headers = [(m.range[-1], m.name) for m in yr.months]
            self.subheaders = [_("W %s") % x[0].strftime('%W') for x in yr.weeks]

        elif self.mode == '3years':
            yr = Year(y)
            yp = yr - 1
            yn = yr + 1

            self.days = yp.days + yr.days + yn.days
            self.title = _("Year %s to Year %s") % (y - 1, y + 1)
            self.selected_day = _get_selection_day(day, self.selected_day, 'year')

            self.headers = [(4, y - 1), (4, y), (4, y + 1)]
            self.subheaders = ['Q1', 'Q2', 'Q3', 'Q4'] * 3

        elif self.mode == '5years':
            yr = Year(y)
            yp1 = yr - 1
            yp2 = yr - 2
            yn1 = yr + 1
            yn2 = yr + 1

            self.days = yp2.days + yp1.days + yr.days + yn1.days + yn2.days
            self.title = _("Year %s to Year %s") % (y - 2, y + 2)
            self.selected_day = _get_selection_day(day, self.selected_day, 'year')

            self.headers = [(2, y - 2), (2, y - 1), (2, y), (2, y + 1), (2, y + 2)]
            self.subheaders = ['H1', 'H2'] * 5

        else:
            month = Month(y, m)
            self.days = [d for d in month]
            self.title = ustr(month)
            self.selected_day = _get_selection_day(day, self.selected_day, 'month')
            self.headers = [(7, _("Week %s") % w[0].strftime('%W')) for w in month.weeks]
            self.subheaders = [d.day for d in month]

        if self.level:
            field = self.level['link']
            fields = rpc.RPCProxy(self.model).fields_get([field])
            self.fields.update(fields)

        self.events = self.get_events(self.days)
        self.groups = self.get_groups(self.events)
        self.groupbox = GroupBox(self.colors, self.color_values, day,
                title=(self.color_field or None) and self.fields[self.color_field]['string'], mode=self.mode)

    def parse(self, root, fields):

        info_fields = []
        attrs = node_attributes(root)

        for node in root.childNodes:
            attrs = node_attributes(node)

            if node.localName == 'field':
                info_fields += [attrs['name']]

            if node.localName == 'level':
                self.level = attrs
                info_fields += self.parse(node, fields)

        return info_fields

    def get_groups(self, events):

        if not self.level:
            return []

        obj = self.level['object']
        field = self.level['link']
        domain = self.level['domain']

        keys = []
        groups = {}
        for evt in events:
            group_id = evt.record[field]
            group_title = 'None'

            if not group_id: # create dummy group
                group_id = 0

            if isinstance(group_id, (list, tuple)):
                group_id, group_title = evt.record[field]
            elif group_id:
                group_id, group_title = rpc.RPCProxy(obj).name_get([group_id], rpc.session.context)[0]

            group = groups.setdefault(group_id, {'id': group_id, 'title': group_title, 'model': obj, 'items': []})

            group['items'].append(evt.record_id)

            if group_id not in keys:
                keys.append(group_id)

        return [groups[i] for i in keys]
