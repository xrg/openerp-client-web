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

from interface import TinyFieldsContainer

from form import Form

class M2O(TinyFieldsContainer):
    template = "tinyerp.widgets.templates.many2one"
    params=['relation', 'field_name', 'field_value', 'text']

    def __init__(self, attrs={}):
        TinyFieldsContainer.__init__(self, attrs)

        self.field_name = self.name
        self.relation = attrs.get('relation', '')

    def set_value(self, value):
        try:
            super(M2O, self).set_value(value[0])
            self.text = unicode(value[-1])
        except:
            pass
