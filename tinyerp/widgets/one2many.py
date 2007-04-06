###############################################################################
#
# Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id: list.py 7 2007-03-23 12:58:38Z ame $
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
    params = ['string', 'id']

    member_widgets = ['screen']
    form = None

    def __init__(self, attrs={}):
        super(O2M, self).__init__(attrs)

        #self.colspan = 4
        #self.nolabel = True

        # get terp dictionary
        terp = cherrypy.request.terp
        terp = terp[self.name.replace('/', '.')]

        self.model = attrs['relation']

        view = attrs.get('views', {})
        mode = str(attrs.get('mode', 'tree,form')).split(',')

        view_mode = mode
        view_mode2 = mode

        if terp: view_mode = terp.view_mode
        if terp: view_mode2 = terp.view_mode2

        ids = attrs['value'] or []
        #if terp: ids = terp.ids

        id = (ids or None) and ids[0]

        if not terp:
            terp = TinyDict()

        terp.model = self.model
        terp.id = id
        terp.ids = ids
        terp.view_mode = view_mode
        terp.view_mode2 = view_mode2
        terp.domain = []
        terp.context = {}

        self.screen = Screen(terp, prefix=self.name, views_preloaded=view)
        self.id = id
