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

from turbogears import view
from tinyerp import rpc

def tg_query(*args, **kw):
    """Returns url querrystring from the provided arguments...
    for example:

    >>> print tg_query('/graph', 'pie', width=100, height=100)
    >>> "/graph/pie?width=100&height=100"

    """
    result = []
    for k, v in kw.items():
        result += ['%s=%s'%(k, v)]

    url = '/'.join([ustr(a) for a in args])
    return ((url or '') and url + '?') + '&'.join(result)

def add_root_vars(root_vars):
    return root_vars.update({'rpc': rpc})

def add_vars(vars):
    from cherrypy import root

    std_vars = {
        'root': root,
        'query': tg_query
    }

    return vars.update(std_vars)

view.root_variable_providers.append(add_root_vars)
view.variable_providers.append(add_vars)
