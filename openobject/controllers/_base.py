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
