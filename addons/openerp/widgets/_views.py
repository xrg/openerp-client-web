from openobject import pooler

from openerp.utils import rpc

import form
import listgrid

__all__ = ["TinyView", "FormView", "ListView",
           "get_view_widget", "get_registered_views"]


class ViewType(type):
    
    def __new__(cls, name, bases, attrs):
        
        obj = super(ViewType, cls).__new__(cls, name, bases, attrs)    
        
        name = attrs.get("_name")
        kind = attrs.get("_type")
        desc = attrs.get("_desc")
        
        if kind:
            pooler.register_object(obj, key=kind, group="view_types", auto_create=True)
            
        return obj


class TinyView(object):
    
    __metaclass__ = ViewType
    
    _name = None
    _type = None
    _desc = None
    _priority = 0
    
    name = property(lambda self: self._name)
    kind = property(lambda self: self._type)
    desc = property(lambda self: self._desc)
    priority = property(lambda self: self._priority)
    
    def __call__(self, screen):
        pass


class FormView(TinyView):
    
    _type = "form"
    _name = _("Form")
    _desc = _("Form view...")
    _priority = 1

    def __call__(self, screen):
        
        widget = form.Form(prefix=screen.prefix,
                           model=screen.model,
                           view=screen.view,
                           ids=(screen.id or []) and [screen.id],
                           domain=screen.domain,
                           context=screen.context,
                           editable=screen.editable,
                           readonly=screen.readonly,
                           nodefault=screen.nodefault, nolinks=screen.link)

        if not screen.is_wizard and screen.ids is None:
            proxy = rpc.RPCProxy(screen.model)
            screen.ids = proxy.search(screen.domain, screen.offset or False, 
                                      screen.limit or False, 0, screen.context)
            screen.count = proxy.search_count(screen.domain, screen.context)

        return widget

class ListView(TinyView):
    
    _type = "tree"
    _name = _("Search")
    _desc = _("Search view...")
    _priority = 0

    def __call__(self, screen):
        
        widget = listgrid.List(screen.name or '_terp_list',
                                    model=screen.model,
                                    view=screen.view,
                                    ids=screen.ids,
                                    domain=screen.domain,
                                    context=screen.context,
                                    view_mode=screen.view_mode,
                                    editable=screen.editable,
                                    selectable=screen.selectable,
                                    offset=screen.offset, limit=screen.limit, 
                                    count=screen.count, nolinks=screen.link)

        screen.ids = widget.ids
        screen.limit = widget.limit
        screen.count = widget.count
            
        return widget
    

def get_view_widget(kind, screen):
    
    pool = pooler.get_pool()
    views = pool.get_group("view_types")
    
    try:
        return views[kind](screen)
    except Exception, e:
        raise
        raise Exception("view '%s' not supported." % kind)


def get_registered_views():
    
    pool = pooler.get_pool()
    views = pool.get_group("view_types")
    
    views = views.items()
    views.sort(lambda a, b: cmp(a[1].priority, b[1].priority))
    
    return views

    

