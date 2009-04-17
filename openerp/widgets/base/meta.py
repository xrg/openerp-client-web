import inspect

from utils import OrderedSet


class WidgetType(type):

    def __new__(cls, name, bases, attrs):

        _update_list_attr(bases, attrs, 'javascript')
        _update_list_attr(bases, attrs, 'css')

        params = _update_list_attr(bases, attrs, 'params')
        members = _update_list_attr(bases, attrs, 'members')
        children = _update_list_attr(bases, attrs, 'children')

        if '__init__' in attrs:
            attrs['__init__'] = post_init(attrs['__init__'])

        return super(WidgetType, cls).__new__(cls, name, bases, attrs)


def _update_list_attr(bases, attrs, name):

    res = []
    for base in bases:
        attr = getattr(base, name, [])
        res.extend(attr)

    attr = attrs.get(name, [])
    res.extend(attr)

    res = attrs[name] = list(OrderedSet(res))

    return res


import threading
from new import instancemethod

def post_init(func):

    def wrapper(self, *args, **kw):

        self.display = instancemethod(lockwidget, self, self.__class__)
        
        if not hasattr(self, '__initstack'):
            self._displaylock = threading.Lock()
            self.__initstack = []
        else:
            self.__initstack.append(1)

        res = func(self, *args, **kw)
        try:
            self.__initstack.pop()
        except IndexError:
            del self.__initstack

            bases = list(inspect.getmro(self.__class__))
            for base in bases:
                try:
                    base.__dict__['post_init'](self, *args, **kw)
                except KeyError:
                    pass

        return res

    return wrapper

def lockwidget(self, *args, **kw):
    "Sets this widget as locked the first time it's displayed."
    gotlock = self._displaylock.acquire(False)
    if gotlock:
        del self.display
        self._locked = True
    output = self.__class__.display(self, *args, **kw)
    if gotlock:
        self._displaylock.release()
    return output


