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

from turbogears.widgets import CompoundWidget

from openerp import tools
from openerp.utils import TinyDict
from openerp.widgets.interface import TinyField

from form import Form

class Record(dict):
    
    def __init__(self, params):
        
        self.params = TinyDict(**params.copy())
        self.params.view_type = 'form'
        
        form = Form().create_form(self.params)
        
        record = self._make_record(form)
        self.clear()
        
        self.update(record.copy())
        self['id'] = params.id or False
             
    def _make_record(self, parent=None):
        parent = parent or self

        for wid in parent.iter_member_widgets():

            if isinstance(wid, TinyField) and wid.name and not wid.name.endswith('/'):
                self[wid.name] = wid.get_value()

            elif isinstance(wid, CompoundWidget):
                self._make_record(wid)
    
        params, data = TinyDict.split(self)
        return data
    
    def expr_eval(self, expr, source=None):
        
        if not isinstance(expr, basestring):
            return expr
        
        d = {}
        for name, value in self.items():
            d[name] = value

        d['current_date'] = time.strftime('%Y-%m-%d')
        d['time'] = time
        d['context'] = self.params.context or {}
        d['active_id'] = self.get('id', False)

        val = tools.expr_eval(expr, d)
        return val

# vim: ts=4 sts=4 sw=4 si et

