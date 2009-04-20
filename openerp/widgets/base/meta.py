import inspect

from openerp.tools import load_template

from utils import OrderedSet


class WidgetType(type):

    def __new__(cls, name, bases, attrs):

        attrs['_cls_children'] = _from_bases(bases, 'children', [])
        #_frozenset_from_bases(attrs, bases, 'javascript')
        #_frozenset_from_bases(attrs, bases, 'css')
        _frozenset_from_bases(attrs, bases, 'params')
        _frozenset_from_bases(attrs, bases, 'members')
        
        if attrs.get('template'):
            attrs['template_c'] = load_template(attrs['template'], attrs['__module__'])

        if '__init__' in attrs:
            attrs['__init__'] = post_init(attrs['__init__'])

        return super(WidgetType, cls).__new__(cls, name, bases, attrs)

def _from_bases(bases, name, default=None):
    for base in bases:
        if hasattr(base, name):
            return getattr(base, name)
    return default

def _frozenset_from_bases(attrs, bases, name):
    items = set(attrs.pop(name, []))
    [items.update(getattr(b, name)) for b in bases if hasattr(b, name)]
    fs = attrs[name] = frozenset(items)
    return fs


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

            self._post_init_prepare_members(*args, **kw)

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


