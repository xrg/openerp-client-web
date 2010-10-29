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

import itertools
import time
import xml.dom.minidom

from openobject.widgets import JSLink, CSSLink
from openobject.i18n.format import format_date_custom

from openerp.utils import rpc, node_attributes
from openerp.widgets import TinyWidget

from _base import ICalendar, TinyCalendar
from utils import Day, Week, Month, Year

class MiniCalendar(TinyWidget):
    template = 'view_calendar/widgets/templates/mini.mako'
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
    template = 'view_calendar/widgets/templates/groups.mako'
    params = ["sorted_colors", "colors", "color_values", "title", "grp_model", "grp_domain", "grp_context"]

    colors = {}
    color_values = []
    title = None
    action = None

    def __init__(self, colors, color_values, selected_day, group_relation={}, title=None, mode='month'):
        super(GroupBox, self).__init__()
        self.colors = colors
        self.sorted_colors = self._color_sort(colors)
        self.color_values = color_values
        self.title = title

        if group_relation.get('relation'):
            self.grp_model = group_relation['relation']
            self.grp_domain = group_relation['domain']
            self.grp_context = group_relation['context']

    def _color_sort(self, colors):
        try:
            key = None
            if colors:
                if isinstance(colors.items()[0][0], basestring):
                    key = lambda x: x[0][0]
                elif isinstance(colors.items()[0][0][0], (int, long)):
                    key = lambda x: x[0][1]

            sorted_colors = sorted(colors.items(), key=key)
        except:
            sorted_colors = sorted(colors.items(), key=None)

        return sorted_colors


class Sidebar(TinyWidget):
    template = 'view_calendar/widgets/templates/sidebar.mako'
    params = ['use_search']
    member_widgets = ['minical', 'groupbox']

    def __init__(self, minical, groupbox, use_search=False):
        super(Sidebar, self).__init__()
        self.minical = minical
        self.groupbox = groupbox
        self.use_search = use_search

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

    template = 'view_calendar/widgets/templates/month.mako'
    params = ['month', 'events', 'selected_day', 'calendar_fields', 'date_format']

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

        minical = MiniCalendar(self.selected_day)
        groupbox = GroupBox(self.colors, self.color_values, self.selected_day,
                group_relation=self.fields[self.color_field],
                title=(self.color_field or None) and self.fields[self.color_field]['string'],
                mode='month')

        self.sidebar = Sidebar(minical, groupbox, self.use_search)


class WeekCalendar(TinyCalendar):
    template = 'view_calendar/widgets/templates/week.mako'
    params = ['week', 'events', 'selected_day', 'calendar_fields', 'date_format']

    week = None
    events = {}

    def __init__(self, model, view, ids=None, domain=[], context={}, options=None):
        TinyCalendar.__init__(self, model, ids, view, domain, context, options)

        y, m, d = time.localtime()[:3]
        if options:
            y, m, d = options.date1[:3]

        self.week = Week(Day(y, m, d))
        self.events = self.get_events(self.week.days)

        self.selected_day = _get_selection_day(Day(y, m, d), self.selected_day, 'week')

        minical = MiniCalendar(self.week[0], True)
        groupbox = GroupBox(self.colors, self.color_values, self.week[0],
                group_relation=self.fields[self.color_field],
                title=(self.color_field or None) and self.fields[self.color_field]['string'],
                mode='week')

        self.sidebar = Sidebar(minical, groupbox, self.use_search)

class DayCalendar(TinyCalendar):
    template = 'view_calendar/widgets/templates/day.mako'
    params = ['day', 'events', 'calendar_fields', 'date_format']

    day = None
    events = {}

    def __init__(self, model, view, ids=None, domain=[], context={}, options=None):
        TinyCalendar.__init__(self, model, ids, view, domain, context, options)

        y, m, d = time.localtime()[:3]
        if options:
            y, m, d = options.date1[:3]

        self.day = Day(y,m,d)

        self.events = self.get_events([self.day])

        minical = MiniCalendar(self.day)
        groupbox =  GroupBox(self.colors, self.color_values, self.day,
                group_relation=self.fields[self.color_field],
                title=(self.color_field or None) and self.fields[self.color_field]['string'],
                mode='day')

        self.sidebar = Sidebar(minical, groupbox, self.use_search)

class GanttCalendar(ICalendar):

    template = 'view_calendar/widgets/templates/gantt.mako'

    params = ['title', 'level', 'groups', 'days', 'events', 'calendar_fields', 'date_format',
              'selected_day', 'mode', 'headers', 'subheaders', 'model', 'ids']
    member_widgets = ['sidebar']

    level = None
    groups = None
    title = None
    days = None
    headers = None
    subheaders = None
    mode = 'week'

    sidebar = None

    css = [CSSLink("view_calendar", 'css/calendar.css'),
           CSSLink("view_calendar", 'css/screen.css'),
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
            self.subheaders = [time.strftime('%H', (y, m, d, i, 0, 0, 1, 1, 0)) for i in range(24)]

        elif self.mode == '3days':
            dp = day - 1
            dn = day + 1
            self.days = [dp, day, dn]
            self.title = u"%s, %s, %s" % (ustr(dp), ustr(day), ustr(dn))
            self.selected_day = day

            self.headers = [(24, ustr(dp)), (24, ustr(day)), (24, ustr(dn))]
            self.subheaders = [time.strftime('%H', (y, 1, 1, i, 0, 0, 1, 1, 0)) for i in range(0, 24, 6)]

        elif self.mode == 'week':
            self.days = [d for d in Week(day)]
            self.title = _("%s, Week %s") % (y, day.strftime("%W"))
            self.selected_day = _get_selection_day(day, self.selected_day, 'week')
            self.headers = [(12, u"%s %s" % (d.month2.name, d.day)) for d in self.days]
            self.subheaders = []
            for x in self.days:
                for i in [0, 12]:
                    self.subheaders.append(time.strftime('%H', (y, 1, 1, i, 0, 0, 1, 1, 0)))

        elif self.mode == '3weeks':
            w = Week(day)
            wp = w - 1
            wn = w + 1
            self.days = wp.days + w.days + wn.days
            self.title = _(u"%s - %s") % (ustr(self.days[0]), ustr(self.days[-1]))
            self.selected_day = _get_selection_day(day, self.selected_day, 'week')
            self.headers = [(7, _("Week %s") % w1[0].strftime('%W')) for w1 in [wp, w, wn]]
            self.subheaders = [format_date_custom(x, "E d") for x in itertools.chain(wp, w, wn)]

        elif self.mode == '3months':
            q = 1 + (m - 1) / 3

            mn = Month(y, q * 3)
            mt = mn.prev()
            mp = mt.prev()

            days = [d for d in mp if d.year == mp.year and d.month == mp.month] \
                 + [d for d in mt if d.year == mt.year and d.month == mt.month] \
                 + [d for d in mn if d.year == mn.year and d.month == mn.month]

            self.days = days
            self.title = _("%s, Qtr %s") % (y, q)
            self.selected_day = _get_selection_day(day, self.selected_day, '3months')

            headers = list(itertools.chain(mp.weeks, mt.weeks, mn.weeks))

            self.headers = [(mp.range[-1], ustr(mp)), (mt.range[-1], ustr(mt)), (mn.range[-1], ustr(mn))]
            self.subheaders = []
            for x in headers:
                x = _("Week %s") % x[0].strftime('%W')
                if x not in self.subheaders:
                    self.subheaders.append(x)

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

        minical = MiniCalendar(day)
        groupbox = GroupBox(self.colors, self.color_values, day,
                group_relation=self.fields[self.color_field],
                title=(self.color_field or None) and self.fields[self.color_field]['string'], mode=self.mode)

        self.sidebar = Sidebar(minical, groupbox, self.use_search)

    def parse(self, root, fields):

        info_fields = []
        attrs = node_attributes(root)

        for node in root.childNodes:
            attrs = node_attributes(node)

            if node.localName == 'field':
                info_fields.append(attrs['name'])

            if node.localName == 'level':
                self.level = attrs
                info_fields += self.parse(node, fields)

        return info_fields

    def get_groups(self, events):

        if not self.level:
            return []

        obj = self.level['object']
        field = self.level['link']

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

            group = groups.setdefault(group_id, {'id': str(group_id), 'title': group_title, 'model': obj, 'items': []})

            group['items'].append(str(evt.record_id))

            if group_id not in keys:
                keys.append(group_id)

        return [groups[i] for i in keys]
