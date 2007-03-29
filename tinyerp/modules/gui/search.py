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

"""
This module implementes search view for a tiny model. Currently it simply displays
list view of the given model.

@todo: implement read search window
"""

from turbogears import expose
from turbogears import widgets
from turbogears import controllers

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp import tools
from tinyerp import widgets as tw
from tinyerp.tinyres import TinyResource

class Search(controllers.Controller, TinyResource):

    def __init__(self):
        pass

    def create(self):
        pass

    @expose(template="tinyerp.modules.gui.templates.search")
    def view(self):
        pass

    @expose()
    def find(self):
        pass

    @expose()
    def cancel(self):
        pass

    @expose()
    def select(self):
        pass
