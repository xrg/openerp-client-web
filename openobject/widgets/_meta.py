import openobject.pooler
import openobject.meta


class WidgetType(type):
    def __new__(typ, name, bases, attrs):
        _frozenset_from_bases(attrs, bases, 'params')
        _frozenset_from_bases(attrs, bases, 'member_widgets')

        return super(WidgetType, typ).__new__(typ, name, bases, attrs)

    def make_widget_key(cls, widget):
        return widget.__module__ + '.' + widget.__name__

    def __init__(cls, name, bases, dct):
        super(WidgetType, cls).__init__(name, bases, dct)
        if openobject.meta.Extends not in bases:
            cls.widget_key = cls.make_widget_key(cls)
            openobject.pooler.register_object(
                    cls, key=cls.widget_key, group='widgets')
            return
        assert len(bases) == 2, "It is only possible to Extend one object at a time, and one object has to be Extended"
        bases = list(bases)
        bases.remove(openobject.meta.Extends)
        base_widget = bases[0]
        openobject.pooler.register_object(
                cls, key=cls.make_widget_key(base_widget), group='widgets')

def _frozenset_from_bases(attrs, bases, name):
    items = set(attrs.pop(name, []))
    for b in bases:
        if hasattr(b, name):
            items.update(getattr(b, name))
    fs = attrs[name] = frozenset(items)
    return fs
