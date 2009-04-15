
import copy
import weakref

from inspect import isclass
from itertools import ifilter, count, chain, izip, ifilterfalse

import cherrypy

from openerp import tools

from openerp.validators import *
from formencode.variabledecode import NestedVariables, variable_decode

from openerp.widgets.meta import WidgetType
from openerp.widgets.utils import OrderedSet
from openerp.widgets.utils import only_if


class WidgetException(RuntimeError):
    msg = "Widget error"
    def __init__(self, msg=None):
        self.msg = msg or self.msg

    def __str__(self):
        return self.msg


class WidgetUnlocked(WidgetException, AttributeError):
    msg = ("The widget is not locked. This method needs to wait until the "
           "widget is fully locked in order to function properly")


class WidgetLocked(WidgetException, AttributeError):
    msg = ("The widget is locked. It's unthread-safe to alter it's attributes "
           "after initialization.")


class WidgetInitialized(WidgetException, AttributeError):
    msg = ("The widget is already initialized, try doing it at the "
           "constructor.")


class WidgetUninitialized(WidgetException, AttributeError):
    msg = ("The widget is uninitialized.")


only_if_initialized = only_if('_is_initialized', True, WidgetUninitialized)
only_if_uninitialized = only_if('_is_initialized', False, WidgetInitialized)
only_if_unlocked = only_if('_is_locked', False, WidgetLocked)


class WidgetBunch(OrderedSet):
    """
    An ordered collection of widgets.
    """

    def __init__(self, iterable=[]):
        self._widgets = {}
        super(WidgetBunch, self).__init__(iterable)

    def __getattr__(self, name):
        try:
            return super(WidgetBunch, self).__getattribute__(name)
        except:
            pass
        return self._widgets[name]

    def __getitem__(self, name):
        return self._widgets[name]

    def add(self, value):
        if not isinstance(value, Widget):
            raise TypeError
        super(WidgetBunch, self).add(value)
        if value in self:
            self._widgets[value._name] = value

    append = add

    def retrieve_resources(self):
        from resource import merge_resources, locations
        resources = dict((k, OrderedSet()) for k in locations)
        for w in self:
            merge_resources(resources, w.retrieve_resources())
        return resources

    def __ne__(self, other):
        return not (self==other)

    def __eq__(self, other):
        try:
            if len(self) == len(other):
                for a,b in izip(other, self):
                    if a!=b:
                        return False
                return True
        except TypeError:
            pass
        return False

    def __repr__(self):
        return repr(self._items)


class Widget(object):

    __metaclass__ = WidgetType

    template = None

    css = []
    javascript = []

    css_class = None
    css_classes = []

    parent = None
    children = []

    params = {
        'ident': 'The identified of this widget',
        'name': 'The name of this widget',
        'css_class': 'Main CSS class for this widget',
        'css_classes': 'List of all CSS classes',
        }

    members = []

    default = None
    strip_name = False

    validator = DefaultValidator()

    _is_initialized = False
    _is_locked = False
    
    def __new__(cls, *args, **kw):
        obj = object.__new__(cls)
        obj.orig_args = args[:]
        obj.orig_kw = kw.copy()
        return obj

    def __init__(self, name=None, parent=None, children=[], **kw):

        # set each keyword args as attribute
        for k, v in kw.iteritems():
            if not k.startswith('_'):
                try:
                    setattr(self, k, v)
                except AttributeError, e:
                    #skip setting the value of a read only property
                    pass

        self._name = name

        for param in self.__class__.params:
            if not hasattr(self, param):
                setattr(self, param, None)

        for member in self.__class__.members:
            if not hasattr(self, member):
                setattr(self, member, None)

        # attache parent
        if parent is not None:
            if parent._is_initialized:
                raise WidgetInitialized
            self.parent = weakref.proxy(parent)
            self.parent.children.add(self)

        # copy mutable class attributes
        for name in ['children', 'css', 'javascript']:
            attr = getattr(self.__class__, name, [])
            setattr(self, name, copy.copy(attr))

        children = children or self.children or []

        # override children if given
        self.c = self.children = WidgetBunch()
        for child in children:
            self._append_child(child)

        self._resources = OrderedSet()

        # Set default css class for the widget
        if not getattr(self, 'css_class', None):
            self.css_class = self.__class__.__name__.lower()

    def _collect_resources(self):
        """picks up resources from self and all children"""
        oset = self._resources
        oset.add_all(chain(*[c._resources for c in self.css]))
        oset.add_all(chain(*[c._resources for c in self.javascript]))
        oset.add_all(chain(*[c._resources for c in self.children]))

    def post_init(self, *args, **kw):

        #append widgets listed in members
        for member in self.members:
            child = getattr(self, member)
            self._append_child(child)

        self._collect_resources()
        self._is_initialized = True
        self._is_locked = False

    @property
    def name(self):
        names = [w._name for w in self.path if not w.strip_name and w._name]
        return '.'.join(reversed(names)) or None

    @property
    def path(self):
        item = self
        while item:
            yield item
            item = item.parent

    @property
    def is_root(self):
        return self.parent is None

    def render(self, value=None, **kw):
        kw = self.prepare_dict(value, kw)
        output = tools.renderer(self.template, self.__module__)(**kw)
        return output

    __call__ = display = render

    def get_default(self):
        if callable(self.default):
            return self.default()
        return self.default

    def prepare_dict(self, value, d):

        value = self.adjust_value(value)

        error = getattr(cherrypy.request, 'validation_exception', None)
        if self.is_root:
            error = d.setdefault('error', error)
        else:
            error = d.setdefault('error', None)

        if error:
            if self.is_root:
                value = getattr(cherrypy.request, 'validation_value', value)
                
        d['value'] = value
        d['c'] = d['children'] = self.children

        self.update_params(d)
        
        d['value_for'] = lambda f: self.value_for(f, d['value'])
        d['params_for'] = lambda f: self.params_for(f, **d)
        d['display_child'] = lambda f: self.display_child(f, **d)
        
        # Compute the final css_class string
        d['css_class']= ' '.join(set([d['css_class'] or ''] + d['css_classes']))

        return d
    
    def value_for(self, item, value):
        name = getattr(item, "name", item)
        if isinstance(value, dict):
            return value.get(name)
        else:
            return None
    
    def params_for(self, item, **params):
        name = getattr(item, "name", item)
        item_params = {}
        for k, v in params.iteritems():
            if isinstance(v, dict):
                if name in v:
                    item_params[k] = v[name]
        return item_params
    
    def display_child(self, item, **params):
        v = self.value_for(item, params.get('value'))
        d = self.params_for(item, **params)
        return item.display(v, **d)

    def update_params(self, d):

        # Populate dict with attrs from self listed at params and members
        for k in ifilterfalse(d.__contains__, chain(self.params, self.members)):
            attr = getattr(self, k, None)
            if attr is not None:
                if isinstance(attr, (list, dict)):
                    attr = copy.copy(attr)
                # Variables that are callable with no args are automatically
                # called here
                elif not isinstance(attr, Widget) and callable(attr):
                    #log.debug("Autocalling param '%s'", k)
                    attr = attr()
            d[k] = attr
            
        if d.get('error'):
            d['css_classes'].append("has_error")

    @only_if_initialized
    def retrieve_resources(self):
        """
        Returns a dict keyed by location with ordered collections of
        resources from this widget and its children as values.
        """
        from resource import locations
        resources = dict((k, OrderedSet()) for k in locations)
        for r in self._resources:
            resources[r.location].add(r)

        return resources

    def validate(self, value, state=None):
        """Validate value using validator if widget has one. If validation fails
        a formencode.Invalid exception will be raised.
        """
        if self.validator:
            try:
                value = self.validator.to_python(value, state)
            except Invalid, error:
                raise
        return value

    def adjust_value(self, value, validator=None):
        """Adjusts the python value sent to :meth:`Widget.display` with
        the validator so it can be rendered in the template.
        """
        
        if value is None:
            value = self.get_default()
            
        validator = validator or self.validator
        if validator and not isinstance(self.validator, Schema):
            try:
                value = validator.from_python(value)
            except Invalid, e:
                # Ignore conversion errors so bad-input is redisplayed
                # properly
                pass
        return value

    @only_if_uninitialized
    def _append_child(self, obj):
        """Append an object as a child"""

        if obj is None:
            return

        if isinstance(obj, Widget):
            self.children.append(obj)
            obj.parent = self
        elif isinstance(obj, list):
            for o in obj:
                self._append_child(o)
        elif isinstance(obj, dict):
            for n, o in obj.iteritems():
                self._append_child(o)
        else:
            raise ValueError("Can only append Widgets or Childs, not %r" % obj)

    @only_if_unlocked
    def __setattr__(self, name, value):
        super(Widget, self).__setattr__(name, value)

    @only_if_unlocked
    def __delattr__(self, name):
        super(Widget, self).__delattr__(name)

    def __ne__(self, other):
        return not (self == other)

    def __eq__(self, other):
        return (
            (getattr(other, '__class__', None) is self.__class__) and
              # Check _name so ancestors are not taken into account
              (other._name == self._name) and
              (other.children == self.children) and (other.orig_kw == self.orig_kw)
            )

    def __repr__(self):
        name = self.__class__.__name__
        return "%s(%r, children=%r, **%r)" % (
            name, self._name, self.children, self.orig_kw
        )

class Form(Widget):

    params = ['action', 'hidden_fields']
    members = ['hidden_fields']

    hidden_fields = []


if __name__ == "__main__":

    w = Widget("A", children=[
            Widget("B", children=[])
            ])

    print w.c.B.name
    print w.c.B.ident
