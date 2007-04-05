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

import re
import cherrypy

def _make_dict(data):
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

            res[k] = [(id and 1, id, _make_dict(v))]

    return res

class TinyDict(dict):
    """A dictionary class that allows accessing it's items as it's attributes.
    It also converts stringified Boolean, None, Number or secuence to python object.
    This class is mainly used by Controllers to get special `_terp_` arguments and
    to generate valid dictionary of data fields from the controller keyword arguments.
    """

    def __init__(self, **kw):
        super(TinyDict, self).__init__(**kw)

    def _eval(self, value):
        if not (isinstance(value, str) or isinstance(value, unicode)):
            return value

        pat = re.compile('^(True|False|None|\d+(\.\d+)?|\[.*?\]|\(.*?\)|\{.*?\})$', re.M)
        if pat.match(value):
            return eval(value)

        return value

    def __setitem__(self, name, value):
        value = self._eval(value)
        super(TinyDict, self).__setitem__(name, value)

    def __getattr__(self, name):
        return self.get(name, None)

    def __setattr__(self, name, value):
        self[name] = value

    @staticmethod
    def split(kwargs):
        """A helper function to extract special parameters from the given kwargs.

        @param kwargs: dict of keyword arguments

        @rtype: tuple
        @return: tuple of dicts, (TinyDict, dict of data)
        """

        terp = TinyDict()
        data = {}

        for n, v in kwargs.items():
            if n.startswith('_terp_'):
                terp[n[6:]] = v
            else:
                data[n] = v

        terp.ids = terp.ids or cherrypy.session.get('_terp_ids', [])

        return terp, _make_dict(data)
