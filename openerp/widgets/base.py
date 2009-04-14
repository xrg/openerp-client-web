
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


class Child(object):
    """
    Prepares a Widget to being attached to a parent Widget.

    Creates a Widget instance with supplied arguments to the constructor when
    called (optionally overriding default arguments).
    
        >>> c = Child(Widget, 'foo')
        >>> w = c()
        >>> w.name
        'foo'

    Parameters can be overriden when called.

        >>> w = c(name='bar')
        >>> w.name
        'bar'

    """
    __slots__ = ("widget_class", "name", "children", "kw")

    def __init__(self, widget_class, name=None, children=[], **kw):
        self.widget_class, self.name  = widget_class, name, 
        self.children, self.kw = children, kw

    def __call__(self, parent=None, **kw):
        kw_ = self.kw.copy()
        kw_.update(name=self.name, parent=parent, children=self.children)
        kw_.update(kw)
        return self.widget_class(**kw_)
    

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

    validator = DefaultValidator
    
    _is_initialized = False
    _is_locked = False
    
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
        self.orig_kw = kw.copy()
        
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

        #also append widgets listed in members
        for member in self.members:
            child = getattr(self, member)
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
        #TODO: generate validation schema for input widgets  
        self._collect_resources()
        self._generate_schema()
        self._is_initialized = True
        self._is_locked = True
    
    @property
    def ident(self):
        """
        The calculated id of the widget. This string will provide a unique
        id for each widget in the tree in a format which allows to re-recreate
        the nested structure.
        Example::

            >>> A = Widget("A", children=[
            ...     Widget("B", children=[
            ...         Widget("C")
            ...         ])
            ...     ])
            ...
            >>> C = A.c.B.c.C
            >>> C.ident
            'A_B_C'
        """
        return '_'.join(reversed(
            [w._name for w in self.path if w._name]
            )) or None
        
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
        return tools.renderer(self.template, self.__module__)(**kw)
    
    __call__ = display = render
    
    def get_default(self):
        if callable(self.default):
            return self.default()
        return self.default
    
    def prepare_dict(self, value, d):
                        
        if value is None:
            value = self.get_default()

        value = self.adjust_value(value)

        error = getattr(cherrypy.request, 'validation_exception', None)
        if self.is_root:
            error = d.setdefault('error', error)
        else:
            error = d.setdefault('error', None)

        if error:
            if self.children:
                self.propagate_errors(d, error)
            if self.is_root:
                value = getattr(cherrypy.request, 'validation_value', value)
        
        d['error_for'] = self._child_error_getter(d['error'])

        # Move args passed to child widgets into child_params
        child_params = d.setdefault('child_params', {})
        for k in d.keys():
            if '.' in k:# or '-' in k:
                child_params[k.lstrip('.')] = d.pop(k)
        
        d['value_for'] = self._child_value_getter(value)
        d['params_for'] = self._child_params_getter(child_params)
                
        d['value'] = value
        d['c'] = d['children'] = self.children
        
        self.update_params(d)
        
        # reset the getters here so update_params has a chance to alter
        # the arguments to children and the value
        d['params_for'] = self._child_params_getter(d['child_params'])
        d['value_for'] = self._child_value_getter(d.get('value'))
        d['display_child'] = self._child_display_getter(d['value_for'], d['params_for'])
        
        # Compute the final css_class string
        d['css_class']= ' '.join(set([d['css_class'] or ''] + d['css_classes']))
        
        return d
    
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

    def propagate_errors(self, parent_kw, parent_error):
        child_params = parent_kw.setdefault('child_params',{})
        if parent_error.error_dict:
            if self.strip_name:
                for c in self.children:
                    for subc in c.children:
                        if hasattr(subc, '_name'):
                            try:
                                e = parent_error.error_dict.pop(subc._name)
                            except KeyError:
                                continue
                            if c._name not in parent_error.error_dict:
                                inv = Invalid("some error", {}, e.state, error_dict={})
                                parent_error.error_dict[c._name] = inv
                            child_errors = parent_error.error_dict[c._name].error_dict
                            child_errors[subc._name] = e
            for k,v in parent_error.error_dict.iteritems():
                child_params.setdefault(k, {})['error'] = v

    def _generate_schema(self):
        """If the widget has children this method generates a `Schema` to validate
        including the validators from all children once these are all known.
        """
        if _has_child_validators(self):
            if isinstance(self.validator, Schema):
                #log.debug("Extending Schema for %r", self)
                self.validator = _update_schema(_copy_schema(self.validator),
                                                self.children)
            elif isclass(self.validator) and issubclass(self.validator, Schema):
                #log.debug("Instantiating Schema class for %r", self)
                self.validator = _update_schema(self.validator(), self.children)
            elif self.validator is DefaultValidator:
                self.validator = _update_schema(Schema(), self.children)

            if self.is_root and hasattr(self.validator, 'pre_validators'):
                #XXX: Maybe add VariableDecoder to every Schema??
                #log.debug("Appending decoder to %r", self)
                self.validator.pre_validators.insert(0, VariableDecoder)
            for c in self.children:
                if c.strip_name:
                    v = self.validator.fields.pop(c._name)
                    merge_schemas(self.validator, v, True)

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
            
    @only_if_initialized
    def clone(self, *args, **kw):
        """
        Returns a cloned version of the widget instance, optionally
        overriding initialization parameters.

        This is the only way to safely "modify" a widget instance.

        Example::

            >>> w = Widget('foo', a=2)
            >>> w.id, w.a
            ('foo', 2)
            >>> w2 = w.clone(a=3)
            >>> w2.id, w2.a
            ('foo', 3)
        """
        return Child(
            self.__class__, self._name, children=self.children, **self.orig_kw
            )(*args, **kw)


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
        validator = validator or self.validator
        if validator and not isinstance(self.validator, Schema):
            try:
                value = validator.from_python(value)
            except Invalid, e:
                # Ignore conversion errors so bad-input is redisplayed
                # properly
                pass
        return value

    def _child_value_getter(self, value):
        
        def getter(item):
            if isinstance(value, dict) and isinstance(item, Widget):
                return value.get(item._name)
            return None

        return getter
    
    def _child_params_getter(self, params):
        
        if isinstance(params, dict):
            params = unflatten_args(params)
                    
        def getter(item):
            if isinstance(params, dict) and isinstance(item, Widget):
                item = item._name
            try:
                return params[item]
            except:
                return {}
        
        return getter
    
    def _child_display_getter(self, value_for, params_for):
        def getter(widget, **kw):
            if isinstance(widget, (basestring, int)):
                widget = self.children[widget]
            child_kw = params_for(widget)
            child_kw.update(kw)
            return widget.display(value_for(widget), **child_kw)
        return getter

    def _child_error_getter(self, error):
        def getter(child):
            try:
                if error and error.error_dict:
                    if isinstance(child, Widget):
                        child = child._name
                    return error.error_dict[child] 
            except IndexError, KeyError:
                pass
            return None
        return getter

    @only_if_uninitialized
    def _append_child(self, obj):
        """Append an object as a child"""
        if isinstance(obj, Widget):
            a = obj._append_to(self)
        elif isinstance(obj, Child):
            obj(self)
        elif isinstance(obj, list):
            for o in obj:
                self._append_child(o)
        elif isinstance(obj, dict):
            for n, o in obj.iteritems():
                self._append_child(o)
        else:
            raise ValueError("Can only append Widgets or Childs, not %r" % obj)

    @only_if_initialized
    def _append_to(self, parent=None):
        return self.clone(parent)
    
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
    


import re

_id_RE = re.compile(r'(\w+)+(?:-(\d))*')
def unflatten_args(child_args):
    new = {}
    for k,v in child_args.iteritems():
        splitted = k.split('.',1)
        id = splitted[0]
        if len(splitted) == 2:
            rest = splitted[1]
            if not id:
                new[rest] = v
                continue
            for_id = new.setdefault(id, {})
            for_id.setdefault('child_params', {})[rest] = v
        else:
            for_id = new.setdefault(id,{})
            for key, val  in v.iteritems():
                for_id.setdefault(key,val)

    convert = set()
    for k,v in new.items():
        m = _id_RE.match(k)
        if not m:
            raise ValueError(
                "%r is not a valid id to reference a child" % k
                )
        id, n = m.groups()
        if n is not None:
            new.pop(k,None)
            convert.add(id)
            for_id = new.setdefault(id, {})
            for_id[int(n)] = v

    for k in convert:
        for_k = new[k]
        l = []
        for n in count():
            l.append(for_k.pop(n, {}))
            if not for_k: break
        new[k] = {'child_params':l}
    return new


#------------------------------------------------------------------------------
# Automatic validator generation functions.
#------------------------------------------------------------------------------
def _has_validator(w):
    try:
        return w.validator is not None
    except AttributeError:
        return False


def _has_child_validators(widget):
    for w in widget.children:
        if _has_validator(w): return True
    return False


def _copy_schema(schema):
    """
    Does a deep copy of a Schema instance
    """
    new_schema = copy.copy(schema)
    new_schema.pre_validators = copy.copy(schema.pre_validators)
    new_schema.chained_validators = copy.copy(schema.chained_validators)
    new_schema.order = copy.copy(schema.order)
    fields = {}
    for k, v in schema.fields.iteritems():
        if isinstance(v, Schema):
            v = _copy_schema(v)
        fields[k] = v
    new_schema.fields = fields
    return new_schema
    
def _update_schema(schema, children):
    """
    Extends a Schema with validators from children. Does not clobber the ones
    declared in the Schema.
    """
    for w in ifilter(_has_validator, children): 
        _add_field_to_schema(schema, w._name, w.validator)
    return schema

def _add_field_to_schema(schema, name, validator):
    """ Adds a validator if any to the given schema """
    if validator is not None:
        if isinstance(validator, Schema):
            # Schema instance, might need to merge 'em...
            if name in schema.fields:
                assert (isinstance(schema.fields[name], Schema), 
                        "Validator for '%s' should be a Schema subclass" % name)
                validator = merge_schemas(schema.fields[name], validator)
            schema.add_field(name, validator)
        elif _can_add_field(schema, name):
            # Non-schema validator, add it if we can...
            schema.add_field(name, validator)
    elif _can_add_field(schema, name):
        schema.add_field(name, DefaultValidator)

def _can_add_field(schema, field_name):
    """
    Checks if we can safely add a field. Makes sure we're not overriding
    any field in the Schema. DefaultValidators are ok to override. 
    """
    current_field = schema.fields.get(field_name)
    return bool(current_field is None or
                isinstance(current_field, DefaultValidator))

def merge_schemas(to_schema, from_schema, inplace=False):
    """ 
    Recursively merges from_schema into to_schema taking care of leaving
    to_schema intact if inplace is False (default).
    """
    if not inplace:
        to_schema = _copy_schema(to_schema)

    # Recursively merge child schemas
    is_schema = lambda f: isinstance(f[1], Schema)
    seen = set()
    for k, v in ifilter(is_schema, to_schema.fields.iteritems()):
        seen.add(k)
        from_field = from_schema.fields.get(k)
        if from_field:
            v = merge_schemas(v, from_field)
            to_schema.add_field(k, v)

    # Add remaining fields if we can
    can_add = lambda f: f[0] not in seen and _can_add_field(to_schema, f[0])
    for field in ifilter(can_add, from_schema.fields.iteritems()):
        to_schema.add_field(*field)
                
    return to_schema

class VariableDecoder(NestedVariables):
    pass


if __name__ == "__main__":
    
    w = Widget("A", children=[
            Widget("B", children=[])
            ])
            
    print w.c.B.name
    print w.c.B.ident
