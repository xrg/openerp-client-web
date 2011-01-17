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
from openobject import pooler

__all__ = ["BaseController"]


class ControllerType(type):

    def __init__(cls, name, bases, attrs):
        super(ControllerType, cls).__init__(name, bases, attrs)
        
        if "path" in attrs and name != "BaseController":
            raise Exception("Can't override 'path' attribute.")

        path = attrs.get("_cp_path")
        if path:
            if not path.startswith("/"):
                raise Exception("Invalid path '%s', should start with '/'." % (path))

            pooler.register_object(cls, key=path, group="controllers")


class BaseController(object):
    __metaclass__ = ControllerType

    _cp_path = None

    def _get_path(self):
        return self._cp_path

    path = property(_get_path)
