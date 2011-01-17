###############################################################################
#
#  Copyright (C) 2007-TODAY OpenERP SA. All Rights Reserved.
#
#  $Id$
#
#  Developed by OpenERP (http://openerp.com) and Axelor (http://axelor.com).
#
#  The OpenERP web client is distributed under the "OpenERP Public License".
#  It's based on Mozilla Public License Version (MPL) 1.1 with following 
#  restrictions:
#
#  -   All names, links and logos of OpenERP must be kept as in original
#      distribution without any changes in all software screens, especially
#      in start-up page and the software header, even if the application
#      source code has been changed or updated or code has been added.
#
#  You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################
from openerp.controllers import SecuredController
from openerp.utils import rpc, TinyDict

from openobject.tools import expose


class View_Log(SecuredController):

    _cp_path = "/openerp/viewlog"

    fields = [
        ('id', _('ID')),
        ('create_uid', _('Creation User')),
        ('create_date', _('Creation Date')),
        ('write_uid', _('Latest Modification by')),
        ('write_date', _('Latest Modification Date')),
        ('uid', _('Owner')),
        ('gid', _('Group Owner')),
        ('level', _('Access Level')),
        ('xmlid',_('Internal module data ID'))
    ]

    @expose(template="/openerp/controllers/templates/view_log.mako")
    def index(self, id=None, model=None):

        values = {}
        if id:
            res = rpc.session.execute('object', 'execute', model,
                                      'perm_read', [id], rpc.session.context)

            for line in res:
                for field, label in self.fields:
                    if line.get(field) and field in ('create_uid','write_uid','uid'):
                        line[field] = line[field][1]

                    values[field] = ustr(line.get(field) or '/')

        return {'values':values, 'fields':self.fields}

# vim: ts=4 sts=4 sw=4 si et
