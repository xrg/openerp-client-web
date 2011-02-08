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
import logging
import urlparse
import cherrypy
from formencode import NestedVariables
import cgitb, sys

def nestedvars_tool():
    if hasattr(cherrypy.request, 'params'):
        cherrypy.request.params = NestedVariables.to_python(cherrypy.request.params or {})

cherrypy.tools.nestedvars = cherrypy.Tool("before_handler", nestedvars_tool)
cherrypy.lowercase_api = True

def csrf_check():
    if not cherrypy.request.method == 'POST': return;

    referer = cherrypy.request.headers.get('Referer', '')
    if not(urlparse.urlsplit(referer).path and referer.startswith(cherrypy.request.base)):
        raise cherrypy.HTTPError(403, "Request Forbidden -- You are not allowed to access this resource.")
cherrypy.tools.csrf = cherrypy.Tool('before_handler', csrf_check)

def cgitb_traceback(ignore=None, severity=logging.DEBUG):
    typ, value, tb = sys.exc_info()
    if ignore and issubclass(typ, tuple(ignore)):
        return
    cherrypy.log(cgitb.text((typ, value, tb)), 'HTTP', severity=severity)
cherrypy.tools.cgitb = cherrypy.Tool('before_error_response', cgitb_traceback)
