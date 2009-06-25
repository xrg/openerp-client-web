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

import os
import copy

from openerp.tools import expose

import cherrypy

from openerp import rpc
from openerp import tools
from openerp import common
from openerp import cache

from openerp.controllers.base import SecuredController
from openerp.utils import TinyDict

import openerp.widgets as tw

class View_Log(SecuredController):

    @expose(template="templates/view_log.mako")
    def index(self, **kw):
        params, data = TinyDict.split(kw)

        id = params.id
        model = params.model
        message = None
        tmp = {}
        todo = []

        if id:
            res = rpc.session.execute('object', 'execute', model, 'perm_read', [id], rpc.session.context)

            for line in res:
                todo = [
                    ('id', _('ID')),
                    ('create_uid', _('Creation User')),
                    ('create_date', _('Creation Date')),
                    ('write_uid', _('Latest Modification by')),
                    ('write_date', _('Latest Modification Date')),
                    ('uid', _('Owner')),
                    ('gid', _('Group Owner')),
                    ('level', _('Access Level'))
                ]
                for (key,val) in todo:
                    if line.get(key) and key in ('create_uid','write_uid','uid'):
                        line[key] = line[key][1]

                    tmp[key] = ustr(line.get(key) or '/')

        if not id:
            message = _("No resource is selected...")

        return dict(tmp=tmp, todo=todo, message=message)

# vim: ts=4 sts=4 sw=4 si et

