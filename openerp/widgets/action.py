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
import datetime

import cherrypy

from openerp import icons
from openerp import tools
from openerp import rpc

import screen
from interface import TinyCompoundWidget
from openerp.utils import TinyDict

class Action(TinyCompoundWidget):
    template = """
    <span xmlns:py="http://purl.org/kid/ns#" py:if="screen" py:replace="screen.display()"/>
    """

    params = ['string']
    member_widgets = ['screen']

    screen = None

    def __init__(self, attrs={}):
        super(Action, self).__init__(attrs)
        self.nolabel = True

        self.act_id=attrs['name']
        res = rpc.session.execute('object', 'execute', 'ir.actions.actions', 'read', [self.act_id], ['type'], rpc.session.context)
        if not res:
            raise _('Action not found !')

        ctx = rpc.session.context.copy()
        ctx['get_binary_size'] = False

        type=res[0]['type']
        self.action = rpc.session.execute('object', 'execute', type, 'read', [self.act_id], False, ctx)[0]

        if 'view_mode' in attrs:
            self.action['view_mode'] = attrs['view_mode']

        if self.action['type']=='ir.actions.act_window':

            if not self.action.get('domain', False):
                self.action['domain']='[]'

            self.context = {'active_id': False, 'active_ids': []}
            self.context.update(eval(self.action.get('context', '{}'), self.context.copy()))

            a = self.context.copy()
            a['time'] = time
            a['datetime'] = datetime
            self.domain = tools.expr_eval(self.action['domain'], a)

            views = dict(map(lambda x: (x[1], x[0]), self.action['views']))
            view_mode = self.action.get('view_mode', 'tree,form').split(',')
            view_ids = map(lambda x: views.get(x, False), view_mode)

            if self.action['view_type']=='form':

                params = TinyDict()
                params.model = self.action['res_model']
                params.id = False
                params.ids = None
                params.view_ids = view_ids
                params.view_mode = view_mode
                params.context = self.context
                params.domain = self.domain
                
                params.offset = params.offset or 0
                params.limit = params.limit or 20

                # get pager vars if set
                if hasattr(cherrypy.request, 'terp_params'):
                    current = cherrypy.request.terp_params
                    current = current.chain_get(self.name or '') or current
                    
                    params.offset = current.offset
                    params.limit = current.limit                    

                self.screen = screen.Screen(params, prefix=self.name, editable=True, selectable=3)
                
            elif self.action['view_type']=='tree':
                pass #TODO
            
# vim: ts=4 sts=4 sw=4 si et

