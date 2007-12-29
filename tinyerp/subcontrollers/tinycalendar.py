###############################################################################
#
# Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
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
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
###############################################################################

import time
import math

from turbogears import expose
from turbogears import controllers

import cherrypy

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp.tinyres import TinyResource
from tinyerp.utils import TinyDict

from form import Form

import tinyerp.widgets.tinycalendar as tc

class TinyCalendar(Form):
    
    @expose()
    def default(self, _arg1, _arg2=None, **kw):
        return self.make(_arg1, _arg2, True, kw)
    
    @expose()
    def get(self, _arg1, _arg2=None, **kw):
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
            
        options.mode = "month"
        
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
            
            if params.id in params.ids:
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
        
        proxy = rpc.RPCProxy(params.model)
        data = {}
        
        data[params.fields['date_start']['name']] = params.starts
        
        if 'date_stop' in params.fields:
            data[params.fields['date_stop']['name']] = params.ends
        elif 'date_delay' in params.fields:
            # convert the end time in hours
            day_length = params.fields['day_length']
            
            ds = tc.utils.parse_datetime(params.starts)
            de = tc.utils.parse_datetime(params.ends)
            
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
        
        res = proxy.write(params.id, data, ctx)
        
        #TODO: return error message if any        
        return dict()

class CalendarPopup(Form):
    
    path = '/calpopup'    # mapping from root
    
    @expose(template="tinyerp.subcontrollers.templates.calpopup")
    def create(self, params, tg_errors=None):        
        params.editable = True
        form = self.create_form(params, tg_errors)       
        return dict(form=form, params=params, show_header_footer=False)

    @expose()
    def get_defaults(self, **kw):
        params, data = TinyDict.split(kw)        
        data = {}
        
        if 'date_stop' in params.fields:            
            if params.fields['date_stop']['kind'] == 'date' and params.ends:
                params.ends = params.ends.split(' ')[0]
                
            data[params.fields['date_stop']['name']] = params.ends
            
        elif 'date_delay' in params.fields:
            # convert the end time in hours
            day_length = params.fields['day_length']
            
            ds = tc.utils.parse_datetime(params.starts)
            de = tc.utils.parse_datetime(params.ends)
            
            tds = time.mktime(ds.timetuple())
            tde = time.mktime(de.timetuple())
            
            n = (tde - tds) / (60 * 60)
            
            if n > day_length:
                d = math.floor(n / 24)
                h = n % 24
                
                n = d * day_length + h
            
            data[params.fields['date_delay']['name']] = n
        
        if params.fields['date_start']['kind'] == 'date' and params.starts:
            params.starts = params.starts.split(' ')[0]
            
        data[params.fields['date_start']['name']] = params.starts
            
        ctx = rpc.session.context.copy()
        ctx.update(params.context or {})
        
        return data