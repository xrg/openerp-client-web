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

from turbojson import jsonify

from turbogears import expose
from turbogears import controllers

from turbogears.i18n import tg_gettext

from openerp import rpc

class JSCatalog(controllers.Controller):

    @expose(content_type="text/javascript")
    def default(self, *args, **kw):
        messages = {}
        try:
            locale = tg_gettext.get_locale()
            messages = tg_gettext.get_catalog(locale=locale)._catalog
            messages.pop("")
        except Exception, e:
            pass
        messages = jsonify.encode(messages)

        return """
var LANG = "%(locale)s";
var MESSAGES = %(messages)s;

function _(key){
    try {
        return MESSAGES[key] || key;
    } catch(e) {}
    return key;
}

""" % dict(locale=locale, messages=messages)

# vim: ts=4 sts=4 sw=4 si et
