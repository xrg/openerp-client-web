from utils import OrderedSet
from openerp.tools import load_template


class WidgetType(type):

    def __new__(cls, name, bases, attrs):
        
        _frozenset_from_bases(attrs, bases, 'params')
        _frozenset_from_bases(attrs, bases, 'member_widgets')
        
        if attrs.get('template'):
            attrs['template_c'] = load_template(attrs['template'], attrs['__module__'])

        return super(WidgetType, cls).__new__(cls, name, bases, attrs)

def _frozenset_from_bases(attrs, bases, name):
    items = set(attrs.pop(name, []))
    [items.update(getattr(b, name)) for b in bases if hasattr(b, name)]
    fs = attrs[name] = frozenset(items)
    return fs

