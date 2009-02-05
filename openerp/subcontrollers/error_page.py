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

import sys
import cgitb

from turbogears import expose
from turbogears import redirect
from turbogears import controllers

import cherrypy

from openerp import rpc
from openerp import tools
from openerp import common

import openerp.widgets as tw

class ErrorPage(controllers.Controller):

    nb = tw.form.Notebook({}, [])

    @expose()
    def index(self, *args, **kw):
        raise redirect('/')

    def render(self):
        etype, value, tb = sys.exc_info()

        if not isinstance(value, common.TinyException):
            return cgitb.html((etype, value, tb))

        return self.__render(value)

    @expose(template="openerp.subcontrollers.templates.error_page")
    def __render(self, value):
        title=value.title
        error=value.message
        maintenance = None

        if isinstance(value, common.TinyError):
            proxy = rpc.RPCProxy('maintenance.contract')
            maintenance = proxy.status()

        return dict(title=title, error=error, maintenance=maintenance, nb=self.nb)

    @expose('json')
    def submit(self, tb, explanation, remarks):
        try:
            res = rpc.RPCProxy('maintenance.contract').send(tb, explanation, remarks)
            if res:
                return dict(message=_('Your problem has been sent to the quality team!\nWe will recontact you after analysing the problem.'))
            else:
                return dict(error=_('Your problem could not be sent to the quality team!\nPlease report this error manually at %s') % ('http://openerp.com/report_bug.html'))
        except Exception, e:
            return dict(error=str(e))

_ep = ErrorPage()

# vim: ts=4 sts=4 sw=4 si et

