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

import cherrypy

def make_dict(data):
    """Generates a valid dictionary from the given data to be used with TinyERP.
    """
    res = {}
    for name, value in data.items():
        names = name.split('/')

        if len(names) > 1:
            res.setdefault(names[0], {}).update({"/".join(names[1:]): value})
        else:
            res[name] = value

    for k, v in res.items():
        if type(v) == type({}):
            #res[k] = make_dict(v)

            id = 0
            if '__id' in v:
                id = int(v.pop('__id'))

            res[k] = [(id and 1, id, make_dict(v))]

    return res

class MyDict(dict):
    """A dictionary class that allows accessing it's items
    as it's attributes.
    """
    def __getattr__(self, name):
        return self.get(name, None)

    def __setattr__(self, name, value):
        self[name] = value

def terp_split(kwargs):
    """A helper function to extract special parameters from the given kwargs.

    @param kwargs: dict of keyword arguments

    @rtype: tuple
    @return: tuple of dicts, (terp, data)
    """

    terp = MyDict()
    data = {}

    for n, v in kwargs.items():
        if n.startswith('_terp_'):
            terp[n[6:]] = v
        else:
            data[n] = v

    terp.id = (terp.id or None) and eval(terp.id)
    terp.ids = cherrypy.session.get('_terp_ids', [])

    terp.domain = eval(terp.domain)
    terp.context = eval(terp.context)
    terp.view_ids = eval(terp.view_ids)
    terp.view_mode = eval(terp.view_mode)
    terp.view_mode2 = eval(terp.view_mode2)

    return terp, make_dict(data)
