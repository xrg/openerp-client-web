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

