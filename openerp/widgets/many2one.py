###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import turbogears as tg

from openerp import rpc
from openerp import common

from interface import TinyField
from form import Form

import validators as tiny_validators

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

class M2O(TinyField):
    template = "openerp.widgets.templates.many2one"
    params=['relation', 'text', 'domain', 'context', 'link', 'readonly']

    domain = []
    context = {}
    link = 1

    def __init__(self, attrs={}):

        super(M2O, self).__init__(attrs)
        self.relation = attrs.get('relation', '')

        self.domain = attrs.get('domain', [])
        self.context = attrs.get('context', {})
        self.link = attrs.get('link')

        self.validator = tiny_validators.many2one()

    def set_value(self, value):
        
        if isinstance(value, (tuple, list)):
            self.default, self.text = value
        else:
            self.default = value
            self.text = get_name(self.relation, self.default)
            
    def update_params(self, d):
        super(M2O, self).update_params(d)
        
        if d['value'] and not d['text']:
            d['text'] = get_name(self.relation, d['value'])
            
# vim: ts=4 sts=4 sw=4 si et

