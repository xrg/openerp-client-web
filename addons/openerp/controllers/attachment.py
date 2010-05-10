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
import base64

from openerp.controllers import SecuredController
from openerp.utils import rpc, common

from openobject.tools import expose


class Attachment(SecuredController):

    _cp_path = "/attachment"

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

            import actions
            return actions.execute(action)
        else:
            raise common.message(_('No record selected! You can only attach to existing record...'))

        return True

    @expose(content_type="application/octet-stream")
    def save_as(self, fname=None, record=False, **kw):
        record = int(record)
        proxy = rpc.RPCProxy('ir.attachment')

        data = proxy.read([record], [], rpc.session.context)
        if len(data) and not data[0]['link'] and data[0]['datas']:
            return base64.decodestring(data[0]['datas'])
        else:
            return ''

    @expose('json')
    def removeAttachment(self, id=False, **kw):
        proxy = rpc.RPCProxy('ir.attachment')
        proxy.unlink(int(id))
        return dict()


# vim: ts=4 sts=4 sw=4 si et

