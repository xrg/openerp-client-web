###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# The OpenERP web client is distributed under the "OpenERP Public License".
# It's based on Mozilla Public License Version (MPL) 1.1 with following
# restrictions:
#
# -   All names, links and logos of Tiny, OpenERP and Axelor must be
#     kept as in original distribution without any changes in all software
#     screens, especially in start-up page and the software header, even if
#     the application source code has been changed or updated or code has been
#     added.
#
# -   All distributions of the software must keep source code with OEPL.
#
# -   All integrations to any other software must keep source code with OEPL.
#
# If you need commercial licence to remove this kind of restriction please
# contact us.
#
# You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################
import cherrypy
from openerp.controllers import SecuredController, actions
from openerp.utils import rpc

from openobject.tools import expose


class Requests(SecuredController):

    _cp_path = "/openerp/requests"

    def my(self):

        if not rpc.session.is_logged():
            return [],[]
        
        ids, ids2 = rpc.RPCProxy('res.request').request_get()

        total_request = 0
            
        if len(ids):
            total_request = len(ids)
            
        return ids, total_request

    @expose()
    def default(self):
        return actions.execute(
            rpc.RPCProxy('ir.actions.act_window')\
                    .for_xml_id('base', 'res_request-act')
        )
