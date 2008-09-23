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

from openerp import rpc
from openerp.tinyres import TinyResource
from openerp.utils import TinyDict
from openerp import common

import openerp.widgets as tw

class Attachment(controllers.Controller, TinyResource):

    @expose(template="openerp.subcontrollers.templates.attachment_list")
    def index(self, model, id, comment='', record=None):

        id = int(id)
        desc = ''
        
        params = TinyDict()
        params.model = 'ir.attachment'
        params.view_mode = ['tree', 'form']

        params.domain = [('res_model', '=', model), ('res_id', '=', id)]

        screen = tw.screen.Screen(params, selectable=1)
        screen.widget.pageable = False
        
        proxy = rpc.RPCProxy('ir.attachment')
        
        if comment and record:
            desc = proxy.write([int(record)], {'description': comment}, rpc.session.context)

        return dict(screen=screen, model=model, desc=desc, id=id, show_header_footer=False)

    @expose(template="openerp.subcontrollers.templates.attachment_form")
    def edit(self, fname='', **kw):
        
        desc = ''
        model = kw.get('model')
        record = kw.get('record')
        id = kw.get('id')
        ext = ''
        
        proxy = rpc.RPCProxy('ir.attachment')
        
        if record:
            record = int(record)
            datas = proxy.read([record])
            desc = datas[0].get('description') or ''
        
        if(fname):
            exten = fname.split('.')[-1].lower()
            if exten in ('jpg', 'jpeg', 'png', 'gif', 'bmp'):
                ext = exten
                
        return dict(model=model, fname=fname, id=id, desc=desc, record=record, ext=ext, show_header_footer=False)
    
    @expose()
    def get_image(self, **kw):
        record = kw.get('record')
        
        proxy = rpc.RPCProxy('ir.attachment')
        datas = proxy.read([record])
        datas = datas[0]

        try:
            if not datas['link']:
                return base64.decodestring(datas['datas'])
        except Exception, e:
            return common.message(_('Unable to preview image file !\nVerify the format.'))

    @expose()
    def save(self, model, id, uploadfile, **kw):

        data = uploadfile.file.read()
        fname = os.path.basename(uploadfile.filename)        
        comment = kw.get('description', '')
        record = kw.get('record', None)

        # XXX: we can't reconise basename of window path on Linux
        if '\\' in fname: # though `\` is valid in Unix path
            fname = fname.split('\\')[-1]

        proxy = rpc.RPCProxy('ir.attachment')

        if data and not record:
            proxy.create({'name': fname, 'datas': base64.encodestring(data), 'datas_fname': fname, 'description': comment, 'res_model': model, 'res_id': int(id)})
        if data and record:
            proxy.write([int(record)], {'name': fname, 'datas': base64.encodestring(data), 'datas_fname': fname, 'description': comment, 'res_model': model, 'res_id': int(id)}, rpc.session.context)

        return self.index(model, id, comment=comment, record=record)

    @expose()
    def delete(self, model, id, record, **kw):
        record = int(record)
        
        proxy = rpc.RPCProxy('ir.attachment')
        proxy.unlink([record])

        return self.index(model, id)

    @expose(content_type="application/octet-stream")
    def save_as(self, fname=None, record=False, **kw):
        
        record = int(record)
        
        ctx = rpc.session.context.copy()
        proxy = rpc.RPCProxy('ir.attachment')
        data = proxy.read([record], [], ctx)
        
        if len(data) and not data[0]['link'] and data[0]['datas']:
            return base64.decodestring(data[0]['datas'])
        else:
            return ''

# vim: ts=4 sts=4 sw=4 si et

