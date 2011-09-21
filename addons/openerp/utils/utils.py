###############################################################################
#
#  Copyright (C) 2007-TODAY OpenERP SA. All Rights Reserved.
#
#  $Id$
#
#  Developed by OpenERP (http://openerp.com) and Axelor (http://axelor.com).
#
#  The OpenERP web client is distributed under the "OpenERP Public License".
#  It's based on Mozilla Public License Version (MPL) 1.1 with following 
#  restrictions:
#
#  -   All names, links and logos of OpenERP must be kept as in original
#      distribution without any changes in all software screens, especially
#      in start-up page and the software header, even if the application
#      source code has been changed or updated or code has been added.
#
#  You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
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
    
    def make_dict_internal(data, is_params=False, previous_dict_ids=None):
        if id(data) in previous_dict_ids:
            raise ValueError("Recursive dictionary detected, _make_dict does not handle recursive dictionaries.")
        previous_dict_ids.add(id(data))
    
        res = (is_params or {}) and TinyDict()
    
        for name, value in data.items():
    
            #XXX: safari 3.0 submits selection field even if no `name` attribute
            if not name:
                continue
    
            if isinstance(name, basestring) and '/' in name:
                names = name.split('/')
                root = names[0]
                if root in res and not isinstance(res[root], dict):
                    del res[root]
                res.setdefault(root, (is_params or {}) and TinyDict()).update({"/".join(names[1:]): value})
            elif name not in res:
                # if name is already in res, it might be an o2m value
                # which tries to overwrite a recursive object/dict
                res[name] = value
    
        for k, v in res.items():
            if isinstance(v, dict):
                if not is_params and '__id' in v:
                    _id = v.pop('__id') or 0
                    _id = int(_id)
    
                    values = _make_dict(v, is_params)
                    if values and any(values.itervalues()):
                        res[k] = [(_id and 1, _id, values)]
                    else:
                        res[k] = []
    
                else:
                    res[k] = make_dict_internal(v, is_params and isinstance(v, TinyDict), previous_dict_ids)
    
        previous_dict_ids.remove(id(data))
        return res
    
    return make_dict_internal(data, is_params, set())


crummy_pseudoliteral_matcher = re.compile('^(True|False|None|-?\d+(\.\d+)?|\[.*?\]|\(.*?\)|\{.*?\})$', re.M)
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

        if crummy_pseudoliteral_matcher.match(value):
            try:
                return openobject.tools.ast.literal_eval(value)
            except ValueError:
                pass
            except SyntaxError:
                # certificates are sequences of digits but may (will?) start
                # with a pair of zeroes, leading to this code trying (and
                # failing) to parse them as integers.
                #
                # Ignore only this case if we catch a syntax error
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

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

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
        from openerp.widgets.form import OneToMany
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
                    o2m_ids = eval(value)
                    if o2m_ids:
                        if not isinstance(o2m_ids, list):
                            o2m_ids = [o2m_ids]

                        from openerp.utils import rpc
                        Relation = rpc.RPCProxy(attrs['relation'])
                        relation_objects = Relation.read(o2m_ids, [], rpc.session.context)
                        relation_fields = Relation.fields_get(False, rpc.session.context)
                        for relation_record in relation_objects:
                            for field_name, field_value in relation_record.items():
                                if field_name in relation_fields and relation_fields[field_name]['type'] == 'many2many':
                                    relation_record[field_name] = [OneToMany.replace_all(*field_value)]

                        value = []
                        for relation_record in relation_objects:
                            id = relation_record.pop('id')
                            value.append(OneToMany.update(id, relation_record))
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
                    converted = v.to_python(value, None)
                else:
                    converted = v.from_python(value, None)
                kw[name] = converted
            except formencode.api.Invalid, e:
                if form and not safe:
                    raise TinyFormError(name.replace('_terp_form/', ''), e.msg, e.value)

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
