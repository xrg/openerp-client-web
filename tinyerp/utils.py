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
from tinyerp.widgets import validators as tw_validators

def _make_dict(data, is_params=False):
    """If is_params is True then generates a TinyDict otherwise generates a valid
    dictionary from the given data to be used with TinyERP.

    @param data: data in the form of {'a': 1, 'b/x': 1, 'b/y': 2}
    @param is_params: if True generate TinyDict instead of standard dict

    @return: TinyDict or dict
    """

    res = (is_params or {}) and TinyDict()

    for name, value in data.items():
        
        if isinstance(name, basestring) and '/' in name:        
            names = name.split('/')
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
        super(TinyDict, self).__init__()
        
        for k, v in kwargs.items():
            self[k] = v

    def _eval(self, value):
        if not isinstance(value, basestring):
            return value

        pat = re.compile('^(True|False|None|-?\d+(\.\d+)?|\[.*?\]|\(.*?\)|\{.*?\})$', re.M)
        if pat.match(value):
            try:
                return eval(value)
            except:
                pass

        return value

    def __setattr__(self, name, value):
        name = '_terp_%s' % name
        value = self._eval(value)
        
        self[name] = value

    def __getattr__(self, name):
        nm = '_terp_%s' % name
        return self.get(nm, self.get(name, None))
    
    def __setitem__(self, name, value):
        value = self._eval(value)
        super(TinyDict, self).__setitem__(name, value)
        
    def chain_get(self, name, default=None):
        names = re.split('\.|/', ustr(name))
        value = super(TinyDict, self).get(names[0], default)

        for n in names[1:]:
            if isinstance(value, TinyDict):
                value = value.get(n, default)

        return value

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
            if n.find('_terp_') > -1:
                params[n] = v
            else:
                data[n] = v

        return _make_dict(params, True), _make_dict(data, False)

class TinyFormError(tg_validators.Invalid):
    def __init__(self, field, msg, value):
        tg_validators.Invalid.__init__(self, msg, value, state=None, error_list=None, error_dict=None)
        self.field = field
               
class TinyForm(TinyDict):
        
    def __init__(self, **kwargs):          
        
        VALIDATORS = {
            'date': tw_validators.DateTime(format="%Y-%m-%d"),
            'time': tw_validators.DateTime(format="%H:%M:%S"),        
            'datetime': tw_validators.DateTime(format="%Y-%m-%d %H:%M:%S"),
            'float_time': tw_validators.Float(),
            'float': tw_validators.Float(),
            'integer': tw_validators.Int(),
            'selection': tw_validators.Selection(),
            'char': tw_validators.String(),
            'boolean': tw_validators.Bool(),
            'reference': tw_validators.Reference(),
            'binary': tw_validators.Binary(),
            'text': tw_validators.String(),
            'text_tag': tw_validators.String(),
            'many2many': tw_validators.many2many(),
            'many2one': tw_validators.many2one(),
            'email' : tw_validators.Email(),
            'url' : tw_validators.Url()
        }
        
        kw = {}
        
        for k, v in kwargs.items():
            if '_terp_' not in k:
                kw['_terp_form/' + k] = eval(v)

        for name, attrs in kw.items():
            
            kind = attrs.get('type', 'char')
            value = attrs.get('value')
                        
            required = attrs.get('required', False)

            if kind not in VALIDATORS:
                kind = 'char'
            
            try:
                v = VALIDATORS[kind]
                #v.not_empty = (required or False) and True
                value = v.to_python(value, None)
            except tg_validators.Invalid, e:
                raise TinyFormError(name.replace('_terp_form/', ''), e.msg, e.value)
            
            kw[name] = value
            
        params, data = TinyDict.split(kw)
        params = params.form
        
        super(TinyForm, self).__init__(**params)

if __name__ == "__main__":
    
    kw = {'_terp_view_ids': "[False, 45]",
          'view_ids/_terp_view_ids': '[False, False]',
          'view_ids/child/_terp_view_ids': '[112, 111]'
    }
    params, data = TinyDict.split(kw)
    
    
    params.domain = "[1]"
    params.setdefault('domain', 'something...')
    params.context = "{}"
    params['context'] = "{'id': False}"
    
    print params
    print params.view_ids
    print params.chain_get('view_ids')
    print params.chain_get('view_ids.child')
    print params.chain_get('view_ids.child').view_ids
    
