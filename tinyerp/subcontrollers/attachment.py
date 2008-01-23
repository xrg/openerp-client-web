###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id$
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

import os
import base64

from turbogears import expose
from turbogears import controllers

from tinyerp import rpc
from tinyerp.tinyres import TinyResource
from tinyerp.utils import TinyDict

import tinyerp.widgets as tw

class Attachment(controllers.Controller, TinyResource):

    @expose(template="tinyerp.subcontrollers.templates.attachment")
    def index(self, model, id):

        id = int(id)

        params = TinyDict()
        params.model = 'ir.attachment'
        params.view_mode = ['tree', 'form']

        params.domain = [('res_model', '=', model), ('res_id', '=', id)]

        screen = tw.screen.Screen(params, selectable=1)
        screen.widget.pageable = False

        return dict(screen=screen, model=model, id=id, show_header_footer=False)

    @expose()
    def add(self, model, id, uploadfile):

        data = uploadfile.file.read()
        fname = os.path.basename(uploadfile.filename)

        # XXX: we can't reconise basename of window path on Linux
        if '\\' in fname: # though `\` is valid in Unix path
            fname = fname.split('\\')[-1]

        if data:
            proxy = rpc.RPCProxy('ir.attachment')
            proxy.create({'name': fname, 'datas': base64.encodestring(data), 'datas_fname': fname, 'res_model': model, 'res_id': id})

        return self.index(model, id)

    @expose()
    def delete(self, model, id, record, **kw):
        record = int(record)

        proxy = rpc.RPCProxy('ir.attachment')
        proxy.unlink([record])

        return self.index(model, id)

    @expose(content_type="application/octat-stream")
    def save(self, fname=None, record=False, **kw):
        record = int(record)

        proxy = rpc.RPCProxy('ir.attachment')
        data = proxy.read([record])

        if len(data) and not data[0]['link'] and data[0]['datas']:
            return base64.decodestring(data[0]['datas'])
        else:
            return ''
