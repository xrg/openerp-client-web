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

from turbogears import validators as tg_validators
from tinyerp.widgets import validators as terp_validators

def _make_dict(data, is_params=False):
    """If is_params is True then generates a TinyDict otherwise generates a valid
    dictionary from the given data to be used with TinyERP.

    @param data: data in the form of {'a': 1, 'b/x': 1, 'b/y': 2}
    @param is_params: if True generate TinyDict instead of standard dict

    @return: TinyDict or dict
    """

    res = (is_params or {}) and TinyDict()

    for name, value in data.items():
        names = name.split('/')

        if len(names) > 1:
            res.setdefault(names[0], (is_params or {}) and TinyDict()).update({"/".join(names[1:]): value})
        else:
            res[name] = value

    for k, v in res.items():
        if isinstance(v, dict):
            if not is_params and '__id' in v:
                id = v.pop('__id') or 0
                id = int(id)

                values = _make_dict(v, is_params)
                if values:
                    res[k] = [(id and 1, id, values)]

            else:
                res[k] = _make_dict(v, is_params and isinstance(v, TinyDict))

    return res

class TinyDict(dict):
    """A dictionary class that allows accessing it's items as it's attributes.
    It also converts stringified Boolean, None, Number or secuence to python object.
    This class is mainly used by Controllers to get special `_terp_` arguments and
    to generate valid dictionary of data fields from the controller keyword arguments.
    """

    def __init__(self, **kwargs):
        super(TinyDict, self).__init__(**kwargs)

    def _eval(self, value):
        if not isinstance(value, basestring):
            return value

        pat = re.compile('^(True|False|None|\d+(\.\d+)?|\[.*?\]|\(.*?\)|\{.*?\})$', re.M)
        if pat.match(value):
            try:
                return eval(value)
            except:
                pass

        return value

    def __setitem__(self, name, value):
        value = self._eval(value)
        super(TinyDict, self).__setitem__(name, value)

    def __getitem__(self, name):
        names = ustr(name).split('.')
        value = self.get(names[0], None)

        for n in names[1:]:
            if isinstance(value, TinyDict):
                value = value.get(n, None)

        return value

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    @staticmethod
    def split(kwargs):
        """A helper function to extract special parameters from the given kwargs.

        @param kwargs: dict of keyword arguments

        @rtype: tuple
        @return: tuple of dicts, (TinyDict, dict of data)
        """

        params = TinyDict()
        data = {}

        for n, v in kwargs.items():
            if n.find('_terp_') != -1:
                n = n.replace('_terp_', '')
                params[n] = v
            else:
                data[n] = v

        return _make_dict(params, True), _make_dict(data, False)

class TinyParent(TinyDict):
    """This class will be used to convert each parent_form values in its python
    equivalent. This method will be used during evaluating context and domain
    which relies on parent form.
    """

    VALS = {
        'char' : terp_validators.String,
        'text': terp_validators.String,
        'integer' : terp_validators.Int,
        'float' : terp_validators.Float,
        'boolean': terp_validators.Bool,
        'selection' : terp_validators.Selection,
        'many2many' : terp_validators.many2many,
        'many2one' : terp_validators.many2one
        }

    def __init__(self, **kwargs):
        kw = kwargs.copy()

        # first generate validator from type type info
        for k, v in kw.items():
            if k.startswith('_terp_parent_types') and v in self.VALS:
                kw[k] = self.VALS[v]()

        # then convert the values into pathon object
        for k, v in kw.items():
            if k.startswith('_terp_parent_form'):
                n = '_terp_parent_types/' + k.replace('_terp_parent_form/', '')
                if n in kw and isinstance(kw[n], tg_validators.Validator):
                    if str(v) == '':
                        kw[k] = kw[n].if_empty
                    else:
                        kw[k] = kw[n].to_python(v, None)

        # now split the kw dict
        params, data = TinyDict.split(kw)

        super(TinyParent, self).__init__(**params.parent_form)
