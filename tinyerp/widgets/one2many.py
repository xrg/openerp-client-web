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

from tinyerp.modules.utils import TinyDict

from interface import TinyCompoundWidget
from screen import Screen

class O2M(TinyCompoundWidget):
    """One2Many widget
    """
    template = "tinyerp.widgets.templates.one2many"
    params = ['string', 'id', 'new_attrs']

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
        is_navigating = params.is_navigating
        
        
        pprefix = ''
        if '/' in self.name:
            pprefix = self.name[:self.name.rindex('/')]
            
        pparams = params[pprefix]
        if (pparams and not pparams.id) or (not pparams and not params.id):
            self.new_attrs = { 'text': _("Save/New"), 'help': 'Save parent and create new record.'}

        # get params for this field
        params = params[self.name.replace('/', '.')]

        self.model = attrs['relation']

        view = attrs.get('views', {})
        mode = str(attrs.get('mode', 'tree,form')).split(',')

        view_mode = mode
        view_mode2 = mode

        if params and params.view_mode: view_mode = params.view_mode
        if params and params.view_mode2: view_mode2 = params.view_mode2

        ids = attrs['value'] or []

        id = (ids or None) and ids[0]

        if params and (params.id in ids or params.id is None):
            if is_navigating:
                id = params.id or id
            else:
                id = params.id

        if not params:
            params = TinyDict()

        params.model = self.model
        params.id = id
        params.ids = ids
        params.view_mode = view_mode
        params.view_mode2 = view_mode2
        params.domain = []
        params.context = {}

        self.screen = Screen(params, prefix=self.name, views_preloaded=view, editable=self.editable, selectable=3)
        self.id = id
        
        if view_mode[0] == 'tree':
            self.screen.widget.pageable=False
            self.id = None
