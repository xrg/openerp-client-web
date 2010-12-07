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
from openerp import validators
from openerp.utils import rpc, expr_eval
from openerp.widgets import TinyInputWidget, InputWidgetLabel, register_widget


__all__ = ["M2O"]


class M2OLabel(InputWidgetLabel):
    template = '/openerp/widgets/form/templates/many2one_label.mako'

class M2O(TinyInputWidget):
    template = "/openerp/widgets/form/templates/many2one.mako"
    params=['relation', 'text', 'domain', 'context', 'link', 'readonly', 'default_focus']

    domain = []
    context = {}
    link = 1

    label_type = M2OLabel

    def __init__(self, **attrs):

        super(M2O, self).__init__(**attrs)
        self.relation = attrs.get('relation', '')

        self.domain = attrs.get('domain', [])
        self.context = attrs.get('context', {})
        self.link = attrs.get('link')
        self.onchange = None # override onchange in js code
        
        self.default_focus = attrs.get('default_focus', 0)
        self.validator = validators.many2one()

    def set_value(self, value):

        if value and isinstance(value, (tuple, list)):
            self.default, self.text = value
        elif value and isinstance(value, basestring):
            self.text = value
        else:
            self.default = value
            self.text = rpc.name_get(self.relation, self.default, rpc.session.context)

    def update_params(self, params):
        super(M2O, self).update_params(params)

        if params['value'] and not params['text']:
            try:
                value = expr_eval(params['value'], {'context':rpc.session.context})
            except:
                value = params['value']
            params['text'] = rpc.name_get(self.relation, value, rpc.session.context)

register_widget(M2O, ["many2one"])

# vim: ts=4 sts=4 sw=4 si et
