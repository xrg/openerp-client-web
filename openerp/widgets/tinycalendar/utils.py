###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import time
import datetime
import calendar

DAY_NAMES = [_('Monday'),
             _('Tuesday'),             
             _('Wednesday'),
             _('Thursday'),
             _('Friday'),
             _('Saturday'),
             _('Sunday')]

MONTH_NAMES = ['',
               _('January'),
               _('February'),
               _('March'),
               _('April'),
               _('May'),
               _('June'),
               _('July'),
               _('August'),
               _('September'),
               _('October'),
               _('November'),
               _('December')]

DT_FORMAT_INFO = {'datetime' : ('%Y-%m-%d %H:%M:%S', datetime.datetime, 0, 6),
                  'date': ('%Y-%m-%d', datetime.date, 0, 3),
                  'time': ('%H:%M:%S', datetime.time, 3, 6)}

def parse_datetime(string):
    """Parse given string to `datetime, date or time` object. The string value
    should be in ISO format. 
    """
    
    if not isinstance(string, basestring):
        raise TypeError('expected string or buffer')

    kind = 'datetime'

    if '-' in string and ':' in string:
        kind = 'datetime'
    elif '-' in string:
        kind = 'date'
    elif ':' in string:
        kind = 'time'
        
    fmt, obj, i, j = DT_FORMAT_INFO[kind]
    return obj(*time.strptime(string, fmt)[i:j])

class Day(datetime.date):

    def __init__(self, year, month, day):
        datetime.date.__init__(self, year, month, day)
        
    def week(self):
        return Week(self)

    def month2(self):
        return Month(self.year, self.month)

    def name(self):
        return DAY_NAMES[calendar.weekday(self.year, self.month, self.day)]
    
    week = property(week)
    month2 = property(month2)
    name = property(name)

    def next(self):
        return self + 1

    def prev(self):
        return self - 1
    
    def __add__(self, value):
        return self.fromordinal(self.toordinal() + value)

    def __sub__(self, value):
        return self.fromordinal(self.toordinal() - value)
    
    def __unicode__(self):
        return '%s %d, %s' % (unicode(MONTH_NAMES[self.month]), self.day, self.year)

    def __str__(self):
        return '%s %d, %s' % (MONTH_NAMES[self.month], self.day, self.year)

class Week(object):

    DAY_NAMES = DAY_NAMES

    def __init__(self, day):

        if not isinstance(day, Day):
            raise TypeError("a 'Day' is required")

        self._day = day

    def days(self):

        y = self._day.year
        m = self._day.month
        d = self._day.day

        wd = calendar.weekday(y, m, d)

        result = []

        for i in range(wd, 0, -1):
            result += [self._day - i]

        for i in range(0, 7 - wd):
            result += [self._day + i]

        return result

    days = property(days)

    def next(self):
        return self + 1

    def prev(self):
        return self - 1

    def __add__(self, value):
        day = self.days[-1] + value * 7
        return Week(day)

    def __sub__(self, value):
        day = self.days[-1] - value * 7
        return Week(day)

    def __getitem__(self, index):
        return self.days[index]
    
    def __iter__(self):
        return iter(self.days)

    def __hash__(self):
        return hash((self.days[0], self.days[-1]))
    
    def __unicode__(self):
        return '%s - %s' % (unicode(self.days[0]), unicode(self.days[-1]))

    def __str__(self):
        return '%s - %s' % (self.days[0], self.days[-1])

    def __repr__(self):
        return 'Week(%s, %s)' % (self.days[0], self.days[-1])

class Month(object):
    """ A calendar month with 42 days (6 weeks with dates from prev/next months)
    """
    
    DAY_NAMES = DAY_NAMES
    MONTH_NAMES = MONTH_NAMES
    
    def __init__(self, year, month):

        self.year = year
        self.month = month
        self.name = MONTH_NAMES[month]
        self._range = calendar.monthrange(year, month)

    def range(self):
        return self._range

    def days(self):
        days = []

        starts = self.range[0]
        first = Day(self.year, self.month, 1)

        for i in range(starts, 0, -1):
            days += [first.fromordinal(first.toordinal() - i)]

        for i in range(42 - starts):
            days += [first.fromordinal(first.toordinal() + i)]

        return days

    def weeks(self):
        weeks = []

        for i in range(0, 42, 7):
            week = Week(self.days[i])
            weeks += [week]

        return weeks

    range = property(range)
    days = property(days)
    weeks = property(weeks)

    def next(self):
        """Get next month.
        """
        return self + 1

    def prev(self):
        """Get previous month.
        """
        return self - 1

    def __add__(self, value):

        y = self.year + ((self.month + value) / 12)
        m = (self.month + value) % 12

        if m == 0:
            y -= 1
            m = 12

        return Month(y, m)

    def __sub__(self, value):

        y = self.year + ((self.month - value) / 12)
        m = (self.month - value) % 12

        if m == 0:
            y -= 1
            m = 12

        return Month(y, m)
    
    def __getitem__(self, index):
        return self.days[index]    

    def __iter__(self):
        return iter(self.days)

    def __hash__(self):
        return hash((self.year, self.month))
    
    def __unicode__(self):
        return '%s %d' % (unicode(self.name), self.year)

    def __str__(self):
        return '%s %d' % (self.name, self.year)

    def __repr__(self):
        return 'Month(%s, %s)'%(self.year, self.month)


class Year(object):

    def __init__(self, year):
        self.year = year
        self.__months = []
        self.__weeks = []
        self.__days = []

    def months(self):
        if self.__months:
            return self.__months

        m = Month(self.year, 1)
        while(m.year == self.year):
            self.__months += [m]
            m = m.next()

        return self.__months

    def weeks(self):
        if self.__weeks:
            return self.__weeks

        w = Week(Day(self.year, 1, 1))
        while (w[0].year == self.year or w[-1].year == self.year):
            self.__weeks += [w]
            w = w.next()

        return self.__weeks
        
    def days(self):
        if self.__days:
            return self.__days

        d = Day(self.year, 1, 1)
        while (d.year == self.year):
            self.__days += [d]
            d = d.next()

        return self.__days

    days = property(days)
    weeks = property(weeks)
    months = property(months)

    def next(self):
        """Get next year
        """
        return self + 1

    def prev(self):
        """Get previous year
        """
        return self - 1

    def __add__(self, value):
        return Year(self.year + value)

    def __sub__(self, value):
        return Year(self.year - value)

    def __getitem__(self, index):
        return self.days[index]

    def __iter__(self):
        return iter(self.days)

    def __hash__(self):
        return hash(self.year)

    def __unicode__(self):
        return unicode(self.year)

    def __str__(self):
        return str(self.year)

    def __repr__(self):
        return "Year %s" % self.year

# vim: ts=4 sts=4 sw=4 si et

