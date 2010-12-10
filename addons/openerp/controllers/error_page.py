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
import cgitb
import sys

import cherrypy
from openerp.utils import rpc, common

from openobject.controllers import BaseController
from openobject.tools import expose, redirect

class ErrorPage(BaseController):

    _cp_path = "/openerp/errorpage"    

    @expose()
    def index(self, *args, **kw):
        raise redirect('/openerp')

    def render(self):
        etype, value, tb = sys.exc_info()

        if isinstance(value, common.Concurrency):
            return self.__render(value)

        if not isinstance(value, common.TinyException):
            return cgitb.html((etype, value, tb))

        return self.__render(value)

    @expose(template="/openerp/controllers/templates/error_page.mako")
    def __render(self, value):

        maintenance = None
        concurrency = False

        all_params = cherrypy.request.params

        title=value.title
        error=value.message

        target = cherrypy.request.path_info or '/openerp/form/save'

        if isinstance(value, common.Concurrency):
            concurrency = True

        if isinstance(value, common.TinyError):
            proxy = rpc.RPCProxy('maintenance.contract')
            maintenance = proxy.status()
            cherrypy.response.headers['X-Maintenance-Error'] = "1"

        return dict(title=title, error=error, maintenance=maintenance,
                    concurrency=concurrency, all_params=all_params, target=target)

    @expose('json')
    def submit(self, tb, explanation, remarks, name, email):
        try:
            res = rpc.RPCProxy('maintenance.contract').send(tb, explanation, remarks, name, email)
            if res:
                return dict(message=_('Your problem has been sent to the quality team\nWe will recontact you after analysing the problem.'))
            else:
                return dict(error=_('Your problem could not be sent to the quality team\nPlease report this error manually at %s') % ('support@openerp.com'))
        except Exception, e:
            return dict(error=str(e))

_ep = ErrorPage()

# vim: ts=4 sts=4 sw=4 si et

