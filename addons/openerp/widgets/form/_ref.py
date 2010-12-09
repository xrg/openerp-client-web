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

from openerp.utils import rpc

from openerp import validators

from openerp.widgets import TinyInputWidget
from openerp.widgets import register_widget

__all__ = ["Reference"]


class Reference(TinyInputWidget):

    template = "/openerp/widgets/form/templates/reference.mako"
    params = ["options", "domain", "context", "text", "relation"]

    options = []

    def __init__(self, **attrs):
        super(Reference, self).__init__(**attrs)
        self.options = attrs.get('selection', [])

        self.domain = attrs.get('domain', [])
        self.context = attrs.get('context', {})

        self.validator = validators.Reference()
        self.onchange = None # override onchange in js code

    def set_value(self, value):
        if value:
            self.relation, self.default = value.split(",")
            self.text = rpc.name_get(self.relation, self.default, rpc.session.context)
        else:
            self.relation = ''
            self.default = ''
            self.text = ''

register_widget(Reference, ["reference"])


# vim: ts=4 sts=4 sw=4 si et
