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

from interface import TinyField
from form import Form
from listgrid import List

from openerp import rpc
import validators as tiny_validators

import many2one

class Reference(TinyField):

    template = "openerp.widgets.templates.reference"
    params = ['options','domain','context', "text", "relation"]

    options = []

    def __init__(self, attrs={}):
        super(Reference, self).__init__(attrs)
        self.options = attrs.get('selection', [])
        self.domain = []
        self.context = {}
        self.validator = tiny_validators.Reference()

    def set_value(self, value):
        if value:
            self.relation, self.default = value.split(",")
            self.text = many2one.get_name(self.relation, self.default)
        else:
            self.relation = ''
            self.default = ''
            self.text = ''
            
# vim: ts=4 sts=4 sw=4 si et

