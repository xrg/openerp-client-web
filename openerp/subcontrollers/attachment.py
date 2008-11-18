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
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import os
import base64

from turbogears import expose
from turbogears import controllers

from openerp import rpc
from openerp.tinyres import TinyResource
from openerp.utils import TinyDict
from openerp.subcontrollers import actions
from openerp import common

import openerp.widgets as tw

class Attachment(controllers.Controller, TinyResource):

    @expose()
    def index(self, model, id):

        id = int(id)
        
        if id:
            ctx = {}
            ctx.update(rpc.session.context.copy())

            action = rpc.session.execute('object', 'execute', 'ir.attachment', 'action_get', ctx)

            action['domain'] = [('res_model', '=', model), ('res_id', '=', id)]
            ctx['default_res_model'] = model
            ctx['default_res_id'] = id
            action['context'] = ctx
            
            return actions.execute(action) 
        else:
            message = str(_('No record selected ! You can only attach to existing record...!'))
            raise common.error(_('Error'), _(message))
        
        return True

# vim: ts=4 sts=4 sw=4 si et

