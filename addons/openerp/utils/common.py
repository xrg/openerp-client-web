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
import openobject.errors

def error(title, msg):
    raise openobject.errors.TinyError(message=msg, title=title or _("Error"))

def warning(msg, title=None):
    raise openobject.errors.TinyWarning(message=msg, title=title or _("Warning"))

def message(msg):
    raise openobject.errors.TinyMessage(message=msg)

def concurrency(msg, title=None, datas=None):
    raise openobject.errors.Concurrency(message=msg, title=title, datas=datas)
