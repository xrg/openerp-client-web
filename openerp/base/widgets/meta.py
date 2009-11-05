import inspect
from new import instancemethod

from utils import OrderedSet
from openerp.tools import load_template


class WidgetType(type):

    def __new__(cls, name, bases, attrs):
        
        _frozenset_from_bases(attrs, bases, 'params')
        _frozenset_from_bases(attrs, bases, 'member_widgets')
        
        if attrs.get('template'):
            attrs['template_c'] = load_template(attrs['template'], attrs['__module__'])
            
        if '__init__' in attrs:
            attrs['__init__'] = post_init(attrs['__init__'])

        return super(WidgetType, cls).__new__(cls, name, bases, attrs)


def _frozenset_from_bases(attrs, bases, name):
    items = set(attrs.pop(name, []))
    [items.update(getattr(b, name)) for b in bases if hasattr(b, name)]
    fs = attrs[name] = frozenset(items)
    return fs


def post_init(func):

    def wrapper(self, *args, **kw):

        if not hasattr(self, '__initstack'):
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

