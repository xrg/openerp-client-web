###############################################################################
#
# Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
###############################################################################

import turbogears as tg

from interface import TinyField
from form import Form
from list import List

from tinyerp import rpc
import validators as tiny_validators

import many2one

class Reference(TinyField):

    template = "tinyerp.widgets.templates.reference"
    params = ['options','domain','context', "text", "ref"]

    options = []

    def __init__(self, attrs={}):
        super(Reference, self).__init__(attrs)
        self.options = attrs.get('selection', [])
        self.domain = []
        self.context = {}
        self.validator = tiny_validators.Reference()


    def set_value(self, value):
        if value:
            self.ref, self.default = value.split(",")
            self.text = many2one.get_name(self.ref, self.default)
        else:
            self.ref = ''
            self.default = ''
            self.text = ''
