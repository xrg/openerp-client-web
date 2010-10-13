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
import itertools
import re

from openerp import validators
import formencode
import openobject


def _make_dict(data, is_params=False):
    """If is_params is True then generates a TinyDict otherwise generates a valid
    dictionary from the given data to be used with OpenERP.

    @param data: data in the form of {'a': 1, 'b/x': 1, 'b/y': 2}
    @param is_params: if True generate TinyDict instead of standard dict

    @return: TinyDict or dict
    """

    res = (is_params or {}) and TinyDict()

    for name, value in data.items():

        #XXX: safari 3.0 submits selection field even if no `name` attribute
        if not name:
            continue

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
                if values and any(values.itervalues()):
                    res[k] = [(id and 1, id, values)]
                else:
                    res[k] = []

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
            if (isinstance(v, dict) and not isinstance(v, TinyDict)):
                v = TinyDict(**v)
            self[k] = v

    def _eval(self, value):

        if isinstance(value, list):
            for i, v in enumerate(value):
                value[i] = self._eval(v)
            return value

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

    def update(self, d=(), **kwargs):
        if isinstance(d, dict):
            seq = d.iteritems()
        else:
            seq = d
        for k, v in itertools.chain(seq, kwargs.iteritems()):
            self[k] = v

    def updateAttrs(self, d=(), **kwattrs):
        """ Updates the TinyDict's attrs in bulk, as if using attr access (rather than item access which can be
        performed via setitem)
        """
        if isinstance(d, dict):
            seq = d.iteritems()
        else:
            seq = d
        for k, v in itertools.chain(seq, kwattrs.iteritems()):
            setattr(self, k, v)

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

    def make_plain(self, prefix=''):

        res = {}

        def _plain(data, prefix):
            for k, v in data.items():
                if isinstance(v, dict) and not k.startswith('_terp_'):
                    _plain(v, prefix + k +'/')
                else:
                    res[prefix + k] = v

        _plain(self, prefix)

        return res

    def make_dict(self):
        res = {}
        for k, v in self.items():
            if isinstance(v, TinyDict):
                v = v.make_dict()
            res[k] = v
        return res

_VALIDATORS = {
    'date': lambda *a: validators.DateTime(kind="date"),
    'time': lambda *a: validators.DateTime(kind="time"),
    'datetime': lambda *a: validators.DateTime(kind="datetime"),
    'float_time': lambda *a: validators.FloatTime(),
    'float': lambda *a: validators.Float(),
    'integer': lambda *a: validators.Int(),
    'selection': lambda *a: validators.Selection(),
    'char': lambda *a: validators.String(),
    'boolean': lambda *a: validators.Bool(),
    'reference': lambda *a: validators.Reference(),
    'binary': lambda *a: validators.Binary(),
    'text': lambda *a: validators.String(),
    'text_tag': lambda *a: validators.String(),
    'many2many': lambda *a: validators.many2many(),
    'one2many': lambda *a: validators.one2many(),
    'many2one': lambda *a: validators.many2one(),
    'email' : lambda *a: validators.Email(),
    'url' : lambda *a: validators.URL(),
    'picture': lambda *a: validators.Binary(),
}

class TinyFormError(formencode.api.Invalid):
    def __init__(self, field, msg, value):
        formencode.api.Invalid.__init__(self, msg, value, state=None, error_list=None, error_dict=None)
        self.field = field

class TinyForm(object):
    """An utility class to convert:

        1. local form data to the server data (throws exception if any)
        2. server data to the local data

    Using validators.
    """

    def __init__(self, **kwargs):

        self.data = {}
        for k, v in kwargs.items():
            if '_terp_' not in k:
                try:
                    v = eval(v)
                except:
                    pass
                self.data['_terp_form/' + k] = v

    def _convert(self, form=True, safe=False):

        kw = {}
        for name, attrs in self.data.items():

            if not isinstance(attrs, dict):
                kw[name] = attrs
                continue

            kind = attrs.get('type', 'char')
            value = attrs.get('value')

            required = attrs.get('required', False)

            if kind == "one2many":
                try:
                    value = eval(value)
                    if value:
                        if not isinstance(value, list):
                            value = [value]
                        from openerp.utils import rpc
                        proxy = rpc.RPCProxy(attrs['relation'])
                        res = proxy.read(value, [], rpc.session.context)
                        res1 = proxy.fields_get(False, rpc.session.context)
                        for values in res:
                            for key, val in values.items():
                                if key in res1.keys():
                                    if res1[key]['type'] == 'many2many':
                                        values[key] = [(6, 0, val)]
                        value = []
                        for r in res:
                            id = r.pop('id')
                            value += [(1, id, r)]
                    else:
                        value = []
                except:
                    pass

            elif kind not in _VALIDATORS:
                kind = 'char'

            v = _VALIDATORS.get(kind, openobject.validators.DefaultValidator)()
            if kind == "float" and attrs.get("digit"):
                v = validators.Float(digit=attrs.get("digit"))
            v.not_empty = (required or False) and True

            try:
                if form:
                    value = v.to_python(value, None)
                else:
                    value = v.from_python(value, None)

            except formencode.api.Invalid, e:
                if form and not safe:
                    raise TinyFormError(name.replace('_terp_form/', ''), e.msg, e.value)

            kw[name] = value


        # Prevent auto conversion from TinyDict
        _eval = TinyDict._eval
        TinyDict._eval = lambda self, v: v

        try:
            params, data = TinyDict.split(kw)
            params = params.form or {}

            return TinyDict(**params)

        finally:
            TinyDict._eval = _eval

    def from_python(self):
        return self._convert(False)

    def to_python(self, safe=False):
        return self._convert(True, safe=safe)



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

# vim: ts=4 sts=4 sw=4 si et
