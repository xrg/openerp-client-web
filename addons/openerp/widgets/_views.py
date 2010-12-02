
import copy
import datetime
import re

from openobject import pooler

from openerp.utils import rpc
from openobject.i18n.format import convert_date_format_in_domain

import form
import listgrid
import listgroup

__all__ = ["TinyView", "FormView", "ListView",
           "get_view_widget", "get_registered_views"]


class ViewType(type):

    def __new__(cls, name, bases, attrs):
        obj = super(ViewType, cls).__new__(cls, name, bases, attrs)

        kind = attrs.get("_type")

        if kind:
            pooler.register_object(obj, key=kind, group="view_types")

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
            limit = screen.limit or 50
            proxy = rpc.RPCProxy(screen.model)
            screen.ids = proxy.search(screen.domain, screen.offset or False,
                                      limit, 0, screen.context)
            if len(screen.ids) < limit:
                screen.count = len(screen.ids)
            else:
                screen.count = proxy.search_count(screen.domain, screen.context)

        return widget

class ListView(TinyView):

    _type = "tree"
    _name = _("Search")
    _desc = _("Search view...")
    _priority = 0

    def __call__(self, screen):
        fields = screen.view['fields']
        screen.domain = convert_date_format_in_domain(screen.domain, fields, screen.context)
        screen.search_domain = convert_date_format_in_domain(screen.search_domain, fields, screen.context)

        if screen.group_by_ctx or screen.context.get('group_by') or screen.context.get('group_by_no_leaf'):
            widget = listgroup.ListGroup(screen.name or '_terp_list',
                                        model=screen.model,
                                        view=screen.view,
                                        ids=screen.ids,
                                        domain=screen.domain,
                                        context=screen.context,
                                        view_mode=screen.view_mode,
                                        editable=screen.editable,
                                        selectable=screen.selectable,
                                        offset=screen.offset, limit=screen.limit,
                                        count=screen.count, nolinks=screen.link,
                                        group_by_ctx=screen.group_by_ctx)
        else:
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
                                    count=screen.count, nolinks=screen.link,
                                    m2m=screen.m2m, o2m=screen.o2m,
                                    default_data=screen.default_value)

        screen.ids = widget.ids
        screen.limit = widget.limit
        screen.count = widget.count

        return widget


def get_view_widget(kind, screen):

    pool = pooler.get_pool()
    Views = pool.get_group("view_types")

    try:
        view = Views[kind]()
    except KeyError, e:
        raise Exception("view '%s' not supported." % kind)

    return view(screen)

def get_registered_views():
    pool = pooler.get_pool()
    Views = pool.get_group("view_types")

    views = [(kind, ViewType()) for kind, ViewType in Views.iteritems()]
    views.sort(lambda a, b: cmp(a[1].priority, b[1].priority))

    return views
