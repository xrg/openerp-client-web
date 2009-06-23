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

from openerp import rpc
from openerp import common

from interface import TinyInputWidget
from form import Form

from openerp import validators

def get_name(model, id):
    id = (id or False) and int(id)
    name = (id or str('')) and str(id)

    if model and id:
        proxy = rpc.RPCProxy(model)

        try:
            name = proxy.name_get([id], rpc.session.context.copy())
            name = name[0][1]
        except common.TinyWarning, e:
            name = _("== Access Denied ==")
        except Exception, e:
            raise e

    return name

class M2O(TinyInputWidget):
    template = "templates/many2one.mako"
    params=['relation', 'text', 'domain', 'context', 'link', 'readonly']

    domain = []
    context = {}
    link = 1

    def __init__(self, **attrs):

        super(M2O, self).__init__(**attrs)
        self.relation = attrs.get('relation', '')

        self.domain = attrs.get('domain', [])
        self.context = attrs.get('context', {})
        self.link = attrs.get('link')
        self.onchange = None # override onchange in js code

        self.validator = validators.many2one()

    def set_value(self, value):

        if value and isinstance(value, (tuple, list)):
            self.default, self.text = value
        else:
            self.default = value
            self.text = get_name(self.relation, self.default)

    def update_params(self, d):
        super(M2O, self).update_params(d)

        if d['value'] and not d['text']:
            d['text'] = get_name(self.relation, d['value'])

# vim: ts=4 sts=4 sw=4 si et

