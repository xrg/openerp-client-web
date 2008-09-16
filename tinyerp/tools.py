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
# along with this program; if not, write to the 
# Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
# Boston, MA  02111-1307, USA.
#
###############################################################################

import os
import time
import datetime as DT

from xml import xpath

# xpath module replaces __builtins__['_'], which breaks TG i18n
import turbogears
turbogears.i18n.tg_gettext.install()

import turbogears as tg

from tinyerp import rpc

def expr_eval(string, context={}):
    context['uid'] = rpc.session.uid
    if isinstance(string, basestring):
        return eval(string, context)
    else:
        return string

def node_attributes(node):
    result = {}
    attrs = node.attributes
    if attrs is None:
        return {}
    for i in range(attrs.length):
        result[attrs.item(i).localName] = attrs.item(i).nodeValue
    return result
    
def get_node_xpath(node):

    pn = node.parentNode
    xp = '/' + node.localName

    if pn and pn.localName and pn.localName != 'view':
        xp = get_node_xpath(pn) + xp

    nodes = xpath.Evaluate(node.localName, node.parentNode)
    xp += '[%s]' % (nodes.index(node) + 1)

    return xp

# vim: ts=4 sts=4 sw=4 si et

