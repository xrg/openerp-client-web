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
import math

from turbogears import expose
from turbogears import controllers

import cherrypy

from openerp import rpc
from openerp import tools
from openerp import common
from openerp import format

from openerp.tinyres import TinyResource
from openerp.utils import TinyDict

from form import Form

import openerp.widgets.tinycalendar as tc

class TinyCalendar(Form):
    
    @expose()
    def mini(self, year, month, forweek=False):
        params = TinyDict()
        
        params.year = year
        params.month = month
        params.forweek = forweek
                
        day = tc.utils.Day(params.year, params.month, 1)
        minical = tc.widgets.MiniCalendar(day, forweek=params.forweek, highlight=False)

        return minical.render()

    @expose()
    def get(self, day, mode, **kw):
        
        params, data = TinyDict.split(kw)
        
        options = TinyDict()
        options.selected_day = params.selected_day
        
        day = time.strptime(day, '%Y-%m-%d') 
        
        options.year = day[0]
        options.month = day[1]
        
        options.date1 = day
        options.mode = mode
        
        if params.colors:
            #options.colors = params.colors
            try:
                options.colors = eval(kw['_terp_colors'])
            except:
                pass
            
        if params.color_values:
            options.color_values = params.color_values
            
        options.search_domain = params.search_domain or []
        options.use_search = params.use_search

        params.kalendar = options
        
        form = self.create_form(params)
        return form.screen.widget.render()
    
    @expose('json')
    def delete(self, **kw):
        
        params, data = TinyDict.split(kw)
        
        error = None
        proxy = rpc.RPCProxy(params.model)
        
        try:
            proxy.unlink([params.id])
        except Exception, e:
            error = ustr(e)
            
        return dict(error=error)
    
    @expose()
    def save(self, **kw):
        params, data = TinyDict.split(kw)
        
        data = {}        
        ds = tc.utils.parse_datetime(params.starts)
        de = tc.utils.parse_datetime(params.ends)
        
        data[params.fields['date_start']['name']] = format.parse_datetime(ds.timetuple())
        
        if 'date_stop' in params.fields:
            data[params.fields['date_stop']['name']] = format.parse_datetime(de.timetuple())
        elif 'date_delay' in params.fields:
            # convert the end time in hours
            day_length = params.fields['day_length']
            
            tds = time.mktime(ds.timetuple())
            tde = time.mktime(de.timetuple())
            
            n = (tde - tds) / (60 * 60)
            
            if n > day_length:
                d = math.floor(n / 24)
                h = n % 24
                
                n = d * day_length + h
            
            data[params.fields['date_delay']['name']] = n
        
        ctx = rpc.session.context.copy()
        ctx.update(params.context or {})
        
        error = None
        proxy = rpc.RPCProxy(params.model)
        
        try:
            res = proxy.write(params.id, data, ctx)
        except Exception, e:
            error = ustr(e)
        
        return dict(error=error)
    
    @expose()
    def duplicate(self, **kw):
        params, data = TinyDict.split(kw)
        
        id = params.id
        ctx = params.context
        model = params.model
        
        proxy = rpc.RPCProxy(model)
        new_id = False
        try:
            new_id = proxy.copy(id, {}, ctx)
        except Exception, e:
            pass

        if new_id:
            params.id = new_id
            params.ids += [int(new_id)]
            params.count += 1
            
        return dict(id=new_id)

    def _get_gantt_records(self, model, ids=None, group=None):

        if group:
            record = {'id': group['id']}
            record['items'] = {'name': group['title']}
            record['action'] = None
            record['target'] = None
            record['icon'] = None
            record['children'] = self._get_gantt_records(model, group['items'])
            return [record]

        proxy = rpc.RPCProxy(model)
        ctx = rpc.session.context.copy()

        records = []
        for id in ids:
            record = {'id': id}
            record['items'] = {'name': proxy.name_get([id], ctx)[0][-1]}
            record['action'] = 'javascript: void(0)'
            record['target'] = None
            record['icon'] = None
            record['children'] = None

            records.append(record)

        return records

    @expose('json')
    def gantt_data(self, **kw):
        params, data = TinyDict.split(kw)
        records = []

        if params.groups:
            for group in params.groups:
                records += self._get_gantt_records(params.model, None, group)
        else:
            records = self._get_gantt_records(params.model, params.ids or [])

        return dict(records=records)

class CalendarPopup(Form):
    
    path = '/calpopup'    # mapping from root
    
    @expose(template="openerp.subcontrollers.templates.calpopup")
    def create(self, params, tg_errors=None):        
        params.editable = True
        
        if params.id and cherrypy.request.path == '/calpopup/view':
            params.load_counter = 2

        form = self.create_form(params, tg_errors)       
        return dict(form=form, params=params, show_header_footer=False)

    @expose()
    def get_defaults(self, **kw):
        params, data = TinyDict.split(kw)        
        data = {}
        
        ds = tc.utils.parse_datetime(params.starts)
        de = tc.utils.parse_datetime(params.ends)
        
        if 'date_stop' in params.fields:            
            kind = params.fields['date_stop']['kind']                
            data[params.fields['date_stop']['name']] = format.format_datetime(de.timetuple(), kind)
            
        elif 'date_delay' in params.fields:
            # convert the end time in hours
            day_length = params.fields['day_length']
            
            tds = time.mktime(ds.timetuple())
            tde = time.mktime(de.timetuple())
            
            n = (tde - tds) / (60 * 60)
            
            if n > day_length:
                d = math.floor(n / 24)
                h = n % 24
                
                n = d * day_length + h
            
            data[params.fields['date_delay']['name']] = n
        
        kind = params.fields['date_start']['kind']            
        data[params.fields['date_start']['name']] = format.format_datetime(ds.timetuple(), kind)

        ctx = rpc.session.context.copy()
        ctx.update(params.context or {})
        
        return data
    
# vim: ts=4 sts=4 sw=4 si et

