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

def render():
    etype, value, tb = sys.exc_info()

    if isinstance(value, common.TinyException):
        return _ep.render(title=value.title, message=value.message, error=isinstance(value, common.TinyError))

    return cgitb.html((etype, value, tb))

class ErrorPage(controllers.Controller):

    _nb = tw.form.Notebook({}, [])

    @expose()
    def index(self, *args, **kw):
        raise redirect('/')

    @expose(template="openerp.subcontrollers.templates.error_page")
    def render(self, title, message, error=None):
        return dict(title=title, message=message, error=error, nb=self._nb)

    @expose('json')
    def submit(self, **kw):
        #TODO: submit maintenance request
        return dict()

_ep = ErrorPage()

# vim: ts=4 sts=4 sw=4 si et

