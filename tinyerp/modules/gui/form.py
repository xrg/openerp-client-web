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
This module implementes view for a tiny model having

    view_type = 'form'
    view_mode = 'form,tree'
"""

import xml.dom.minidom

from elementtree import ElementTree as ET

from turbogears import expose
from turbogears import widgets

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp import tools
from tinyerp import widgets as tw

@expose(template="tinyerp.modules.gui.templates.form")
def create(view_id, model, id=None, domain=[], view_ids=[], context={}, message=None):
    """Create view for the given model.

    @param view_id: view id
    @param model: the model
    @param id: record id
    @param domain: the domain
    @param view_ids: view ids
    @param context: the context
    @param message: the message to display

    @return: view of the model (XHTML)
    """    

    form = tw.form.Form(prefix='', view_id=view_id, model=model, id=id, view_ids=view_ids, domain=domain, context=context)
    return dict(message=message, view_id=view_id, model=model, id=id, form=form)
