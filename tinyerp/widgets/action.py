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
from tinyerp import icons
from tinyerp import tools
from tinyerp import rpc

import screen
from interface import TinyCompoundWidget
from tinyerp.modules.utils import TinyDict

class Action(TinyCompoundWidget):
    template = """<span xmlns:py="http://purl.org/kid/ns#">
    <div class="toolbar">
        <table>
            <tr>
                <td width="100%" py:content="string"></td>
                <td>
                    <button type="button" onclick="alert('not implemented yet...')">Find</button>
                    <button type="button" onclick="alert('not implemented yet...')">Open</button>
                    <button type="button" onclick="alert('not implemented yet...')">Switch</button>
                </td>
            </tr>
        </table>
    </div>
    <div class="spacer"/>
    <span py:if="screen" py:replace="screen.display()"/>
    </span>
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
            raise 'ActionNotFound'

        type=res[0]['type']
        self.action = rpc.session.execute('object', 'execute', type, 'read', [self.act_id], False, rpc.session.context)[0]

        if 'view_mode' in attrs:
            self.action['view_mode'] = attrs['view_mode']

        if self.action['type']=='ir.actions.act_window':

            if not self.action.get('domain', False):
                self.action['domain']='[]'

            self.context = {'active_id': False, 'active_ids': []}
            self.context.update(eval(self.action.get('context', '{}'), self.context.copy()))

            a = self.context.copy()
            a['time'] = time
            self.domain = tools.expr_eval(self.action['domain'], a)

            view_id = []
            if self.action['view_id']:
                view_id = [self.action['view_id'][0]]

            if self.action['view_type']=='form':
                mode = (self.action['view_mode'] or 'form,tree').split(',')

                params = TinyDict()
                params.model = self.action['res_model']
                params.id = None
                params.ids = None
                params.view_ids = view_id
                params.view_mode = mode
                params.view_mode2 = mode
                params.context = self.context
                params.domain = self.domain

                self.screen = screen.Screen(params, prefix=self.name)

            elif self.action['view_type']=='tree':
                pass #TODO
