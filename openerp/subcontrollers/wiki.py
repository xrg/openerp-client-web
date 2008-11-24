###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id: viewlist.py 1811 2008-04-17 09:13:58Z ame $
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

import kid
from turbogears import expose
from turbogears import controllers
from turbogears import redirect
from turbogears import validate

from openerp import rpc
from openerp.tinyres import TinyResource
from openerp.utils import TinyDict

import openerp.widgets as tw

from pyparsing import *
import form

class WikiView(controllers.Controller, TinyResource):
    path = '/wiki' 
    @expose(content_type='application/octet')
    def getImage(self, *kw, **kws):
        model = 'ir.attachment'
        field = 'datas_fname'
        file = kws.get('file').replace("'",'').strip()
        #id = kws.get('id')
        proxy = rpc.RPCProxy(model)
        ids = proxy.search([(field,'=',file), ('res_model','=','wiki.wiki')])
        res = proxy.read(ids, ['datas'])[0]
        res = res.get('datas')
        return base64.decodestring(res)
