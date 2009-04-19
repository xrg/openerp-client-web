import re
import collections

from openerp import tools

def only_if(attribute, value=None, exc=Exception):

    def func_wrapper(func):

        callback = attribute
        if not callable(callback):
            callback = lambda self: getattr(self, attribute, None) == value

        def wrapper(self, *args, **kw):
            if callback(self):
                return func(self, *args, **kw)
            raise exc

        return tools.decorated(wrapper, func)

    return func_wrapper

class Enum(set):

    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError


class OrderedSet(set):

    def __init__(self, iterable=[]):

        self._items = items = []

        for item in iterable:
            self.add(item)

    def __contains__(self, value):
        return value in self._items

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def add(self, value):
        if value not in self._items:
            self._items.append(value)

    def add_all(self, values):
        [self.add(value) for value in values]

    def discard(self, value):
        if value in self._items:
            self._items.remove(value)


class Bunch(dict):
    __setattr__ = dict.__setitem__

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError(name)

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


def make_bunch(d):
    """Converts a dict instance into a Bunch"""
    return Bunch(d)


_id_RE = re.compile(r'(\w+)+(?:-(\d))*')
def unflatten_args(child_args):
    new = {}
    for k,v in child_args.iteritems():
        splitted = k.split('.',1)
        id = splitted[0]
        if len(splitted) == 2:
            rest = splitted[1]
            if not id:
                new[rest] = v
                continue
            for_id = new.setdefault(id, {})
            for_id.setdefault('child_args', {})[rest] = v
        else:
            for_id = new.setdefault(id,{})
            for key, val  in v.iteritems():
                for_id.setdefault(key,val)

    convert = set()
    for k,v in new.items():
        m = _id_RE.match(k)
        if not m:
            raise ValueError(
                "%r is not a valid id to reference a child" % k
                )
        id, n = m.groups()
        if n is not None:
            new.pop(k,None)
            convert.add(id)
            for_id = new.setdefault(id, {})
            for_id[int(n)] = v

    for k in convert:
        for_k = new[k]
        l = []
        for n in count():
            l.append(for_k.pop(n, {}))
            if not for_k: break
        new[k] = {'child_args':l}
    return new


