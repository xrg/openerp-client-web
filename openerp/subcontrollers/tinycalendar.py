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
    def default(self, _arg1, _arg2=None, **kw):
        return self.make(_arg1, _arg2, True, kw)
    
    @expose()
    def get(self, _arg1, _arg2=None, **kw):
        return self.make(_arg1, _arg2, False, kw)

    #TODO: reimplement get/make to support gantt
    @expose()
    def gantt(self, _arg1, _arg2=None, **kw):
        kw = kw.copy()
        kw['mode'] = 'gantt'
        return self.make(_arg1, _arg2, False, kw)
    
    @expose()
    def mini(self, year, month, forweek=False):
        params = TinyDict()
        
        params.year = year
        params.month = month
        params.forweek = forweek
                
        day = tc.utils.Day(params.year, params.month, 1)
        minical = tc.widgets.MiniCalendar(day, forweek=params.forweek, highlight=False)

        return minical.render()

    def make(self, _arg1, _arg2=None, _full=False, kw={}):
        
        params, data = TinyDict.split(kw)
        
        if '-' in _arg1:
            _arg1 = time.strptime(_arg1, '%Y-%m-%d')

        if _arg2 and '-' in _arg2:
            _arg2 = time.strptime(_arg2, '%Y-%m-%d')

        options = TinyDict()        
        options.selected_day = params.selected_day 
        
        if isinstance(_arg1, basestring):
            options.year = _arg1
            options.month = _arg2
        else:
            options.year = _arg1[0]
            options.month = _arg1[1]

        options.date1 = None
        options.date2 = None
        
        if not isinstance(_arg1, basestring):     
            options.date1 = _arg1
        
        if not isinstance(_arg2, basestring):
            options.date2 = _arg2
            
        options.mode = kw.get('mode', 'month')
        
        if options.date1:            
            if options.date2:
                options.mode = "week"
            else:
                options.mode = "day"                                    

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
        
        if _full:
            return self.create(params)
        
        form = self.create_form(params)        
        return form.screen.widget.render()
    
    @expose()
    def delete(self, _arg1, _arg2=None, **kw):
        params, data = TinyDict.split(kw)
        
        proxy = rpc.RPCProxy(params.model)
        
        idx = -1
        if params.id:
            res = proxy.unlink([params.id])
            
            if params.ids and params.id in params.ids:
                idx = params.ids.index(params.id)
                params.ids.remove(params.id)
                params.count = 0 # invalidate count

                if idx == len(params.ids):
                    idx = -1

        params.id = (params.ids or None) and params.ids[idx]
        
        kw['_terp_ids'] = ustr(params.ids)
        
        return self.make(_arg1, _arg2, False, kw)
    
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

