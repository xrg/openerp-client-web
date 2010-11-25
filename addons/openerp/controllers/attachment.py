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
import base64

import cherrypy
from openerp.controllers import SecuredController
from openerp.utils import rpc, common, TinyDict

from openobject.tools import expose, redirect

import actions


class Attachment(SecuredController):

    _cp_path = "/openerp/attachment"

    @expose()
    def index(self, model, id):

        id = int(id)

        if id:
            ctx = dict(rpc.session.context)

            action = dict(
                rpc.RPCProxy('ir.attachment').action_get(ctx),
                domain=[('res_model', '=', model), ('res_id', '=', id)],
                context=dict(ctx,
                             default_res_model=model,
                             default_res_id=id
            ))

            return actions.execute(action)
        else:
            raise common.message(_('No record selected, You can only attach to existing record...'))

    @expose(content_type="application/octet-stream")
    def get(self, record=False):
        record = int(record)
        attachment = rpc.RPCProxy('ir.attachment').read(record, [], rpc.session.context)

        if attachment['type'] == 'binary':
            cherrypy.response.headers["Content-Disposition"] = 'attachment; filename="%s"' % attachment['name']
            return base64.decodestring(attachment['datas'])
        elif attachment['type'] == 'url':
            raise redirect(attachment['url'])
        raise Exception('Unknown attachment type %(type)s for attachment name %(name)s' % attachment)

    @expose('json', methods=('POST',))
    def save(self, datas, **kwargs):
        params, data = TinyDict.split(cherrypy.session['params'])
        ctx = dict(rpc.session.context,
                   default_res_model=params.model, default_res_id=params.id,
                   active_id=False, active_ids=[])

        attachment_id = rpc.RPCProxy('ir.attachment').create({
            'name': datas.filename,
            'datas': base64.encodestring(datas.file.read()),
        }, ctx)
        return {'id': attachment_id, 'name': datas.filename}

    @expose('json', methods=('POST',))
    def remove(self, id=False, **kw):
        proxy = rpc.RPCProxy('ir.attachment')
        try:
            proxy.unlink([int(id)], rpc.session.context)
            return {}
        except Exception, e:
            return {'error': ustr(e)}


# vim: ts=4 sts=4 sw=4 si et

