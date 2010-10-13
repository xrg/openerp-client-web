class Enum(set):

    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError


class OrderedSet(set):

    def __init__(self, iterable=None):
        self._items = []

        for item in (iterable or []):
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
        for value in values: self.add(value)

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
