import inspect
import openobject.pooler
import openobject.meta


class WidgetType(type):

    def __new__(cls, name, bases, attrs):

        _frozenset_from_bases(attrs, bases, 'params')
        _frozenset_from_bases(attrs, bases, 'member_widgets')

        if '__init__' in attrs:
            attrs['__init__'] = post_init(attrs['__init__'])

        return super(WidgetType, cls).__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, dct):
        super(WidgetType, cls).__init__(name, bases, dct)
        if not openobject.meta.Extends in bases:
            widget_key = cls.__module__ + '.' + cls.__name__
            cls.widget_key = widget_key
            openobject.pooler.register_object(
                    cls, key=widget_key, group='widgets')
            return
        assert len(bases) == 2, "It is only possible to Extend one object at a time, and one object has to be Extended"
        bases = list(bases)
        bases.remove(openobject.meta.Extends)
        base_widget = bases[0]
        openobject.pooler.register_object(
                cls, key=base_widget.__module__ + '.' + base_widget.__name__, group='widgets')

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
