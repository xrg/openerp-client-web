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

import turbogears as tg
import cherrypy

from tinyerp.utils import TinyDict

from interface import TinyCompoundWidget
from screen import Screen

class O2M(TinyCompoundWidget):
    """One2Many widget
    """
    template = "tinyerp.widgets.templates.one2many"
    params = ['string', 'id', 'readonly', 'parent_id', 'new_attrs', 'pager_info', 'switch_to']

    member_widgets = ['screen']
    form = None

    def __init__(self, attrs={}):
        #FIXME: validation error in `Pricelist Version`
        attrs['required'] = False

        super(O2M, self).__init__(attrs)

        self.new_attrs = { 'text': _("New"), 'help': 'Create new record.'}

#        self.colspan = 4
#        self.nolabel = True

        # get top params dictionary
        params = cherrypy.request.terp_params

        pprefix = ''
        if '/' in self.name:
            pprefix = self.name[:self.name.rindex('/')]

        pparams = params.chain_get(pprefix)
        if (pparams and not pparams.id) or (not pparams and not params.id):
            self.new_attrs = { 'text': _("Save/New"), 'help': 'Save parent and create new record.'}
            
        self.parent_id = params.id
        if pparams:
            self.parent_id = pparams.id

        # get params for this field
        params = params.chain_get(self.name)

        self.model = attrs['relation']
        self.link = attrs['link']

        view = attrs.get('views', {})
        mode = str(attrs.get('mode', 'tree,form')).split(',')

        view_mode = mode
        view_type = mode[0]

        if not params:
            params = TinyDict()

        if params.view_mode: view_mode = params.view_mode
        if params.view_type: view_type = params.view_type

        self.switch_to = view_mode[-1]
        if view_type == view_mode[-1]: self.switch_to = view_mode[0]

        ids = attrs['value'] or []
        id = (ids or None) and ids[0]

        if params:
            id = params.id

        id = id or None

        params.model = self.model
        params.id = id
        params.ids = ids
        params.view_mode = view_mode
        params.view_type = view_type
        params.domain = []
        params.context = {}
        
        if params.view_type == 'tree' and self.readonly:
            self.editable = False
            
        self.screen = Screen(params, prefix=self.name, views_preloaded=view, editable=self.editable, selectable=3, nolinks=self.link)
        self.id = id

        if view_type == 'tree':
            self.screen.widget.pageable=False
            self.id = None

        pager_info = None
        if view_type == 'form':
            c = (self.screen.ids or 0) and len(self.screen.ids)
            i = 0

            if c and self.screen.id in self.screen.ids:
                i = self.screen.ids.index(self.screen.id) + 1

            self.pager_info = '[%s/%s]' % (i, c)
