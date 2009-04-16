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


