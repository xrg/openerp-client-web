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
# -   All names, links and logos of Tiny, Open ERP and Axelor must be
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
from openerp.controllers import SecuredController
from openerp.utils import rpc

from openobject.tools import expose


class Requests(SecuredController):

    _cp_path = "/openerp/requests"

    def my(self):

        if not rpc.session.is_logged():
            return [],[]

        ids, ids2 = cherrypy.session.get('terp_requests', (False, False))
        if ids == False:
            ids, ids2 = rpc.RPCProxy('res.request').request_get()
            cherrypy.session['terp_requests'] = (ids, ids2)

        msg = _("No request")
        if len(ids):
            msg = _('%s request(s)') % len(ids)

        if len(ids2):
            msg += _(' - %s pending request(s)') % len(ids2)

        return ids, msg

    @expose()
    def default(self):
        import actions
        return actions.execute_window(False, 'res.request', res_id=None,
            domain=[('act_to','=',rpc.session.uid)], view_type='form', mode='tree,form')


# vim: ts=4 sts=4 sw=4 si et
