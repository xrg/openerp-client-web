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

from screen import Screen

class ViewForm(tg.widgets.Form):
    template = "tinyerp.widgets.templates.form"
    member_widgets = ['screen']

    def __init__(self, model, id=None, ids=[], state='', view_ids=[], view_mode=['form', 'tree'], view_mode2=['tree', 'form'], domain=[], context={}):
        super(ViewForm, self).__init__(name="view_form")

        if view_mode[0] != view_mode2[0]:
            view_ids = [False] + view_ids
        else:
            if False in view_ids: view_ids.remove(False)

        cherrypy.request.terp_fields = []

        self.screen = Screen(prefix='', model=model, id=id, ids=ids, view_ids=view_ids, view_mode=view_mode, domain=domain, context=context, editable=True)

        self.screen.state = state #TODO: maintain states
        self.screen.view_mode2 = view_mode2

        cherrypy.session['_terp_ids'] = self.screen.ids

        self.fields = cherrypy.request.terp_fields

    def validate(self, value, state=None):
        return super(ViewForm, self).validate(value, state)
