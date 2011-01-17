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

"""
This modules implements custom authorization logic for the OpenERP Web Client.
"""
import types

from openobject.controllers import BaseController
from utils import secured

__all__ = ["SecuredController"]

class SecuredController(BaseController):

    def __getattribute__( self, name ):
        value= object.__getattribute__(self, name)

        if isinstance(value, types.MethodType ) and hasattr(value, "exposed") and not (hasattr(value, "secured") and not value.secured):
            return secured(value)

        # Some other property
        return value


# vim: ts=4 sts=4 sw=4 si et

