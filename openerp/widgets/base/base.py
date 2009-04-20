
import copy
import weakref

from inspect import isclass
from itertools import ifilter, count, chain, izip, ifilterfalse

import cherrypy

from openerp import tools

from openerp.validators import *
from formencode.variabledecode import NestedVariables, variable_decode

from meta import WidgetType
from utils import unflatten_args
from utils import OrderedSet
from utils import only_if, make_bunch


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
        'name': 'The Name for this Widget.',
        'css_class': 'Main CSS class for this widget',
        'css_classes': 'List of all CSS classes',
    }

    members = []

    default = None

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

        # attache parent
        if parent is not None:
            if parent._is_initialized:
                raise WidgetInitialized
            self.parent = weakref.proxy(parent)
            self.parent.children.add(self)
            
        # Append children passed as args or defined in the class, former 
        # override later
        self.c = self.children = WidgetBunch()
        if not [self._append_child(c) for c in children]:
            [obj._append_child(c) for c in self.__class__._cls_children]
            
        # Copy mutable attrs from __class__ into self, if not found in self 
        # set to None
        for name in chain(self.__class__.params, self.__class__.members, ['css', 'javascript']):
            try:
                attr = getattr(self, name, None)
                if isinstance(attr, (list, dict)):
                    attr = copy.copy(attr)
                setattr(self, name, attr)
            except AttributeError, e:
                pass

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

    def _post_init_prepare_members(self, *args, **kw):
        #append widgets listed in members
        for member in self.members:
            child = getattr(self, member)
            self._append_child(child)

    def post_init(self, *args, **kw):
        self._collect_resources()
        self._is_initialized = True
        self._is_locked = False

    @property
    def name(self):
        names = [w._name for w in self.path if w._name]
        return '.'.join(reversed(names)) or None

    @property
    def identifier(self):
        name = self.name
        if not name:
            return name
        return name.replace('.', '_')

    @property
    def path(self):
        item = self
        while item:
            yield item
            item = item.parent

    @property
    def is_root(self):
        return self.parent is None
    
    @property
    def children_deep(self):
        return self.children

    def ifilter_children(self, filter):
        """
        Returns an iterator for all children applying a filter to them.
        """
        return ifilter(filter, self.children)

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

        if value is None:
            value = self.get_default()
        d['value'] = value
                            
        # Move args passed to child widgets into child_args
        child_args = d.setdefault('child_args', {})
        for k in d.keys():
            if '.' in k:# or '-' in k:
                child_args[k.lstrip('.')] = d.pop(k)
        
        d['args_for'] = self._get_child_args_getter(child_args)
        d['value_for'] = self._get_child_value_getter(d['value'])        
        d['c'] = d['children'] = self.children

        d = make_bunch(d)
        self.update_params(d)
        
        # Compute the final css_class string
        d['css_class'] = ' '.join(set([d['css_class'] or ''] + d['css_classes']))

        # reset the getters here so update_params has a chance to alter
        # the arguments to children and the value
        d['args_for'] = self._get_child_args_getter(d['child_args'])
        d['value_for'] = self._get_child_value_getter(d.get('value'))
        # Provide a shortcut to display a child field in the template
        d['display_child'] = self._child_displayer(self.children,
                                                   d['value_for'],
                                                   d['args_for'])

        return d
    
    def _get_child_value_getter(self, value):
        def value_getter(child_id):
            if value:
                if isinstance(child_id, Widget) and isinstance(value, dict):
                    child_id = child_id._name
                try:
                    return value[child_id]
                except (IndexError, KeyError, TypeError):
                    None
        return value_getter

    def _get_child_args_getter(self, child_args):
        if isinstance(child_args, dict):
            child_args = unflatten_args(child_args)
        def args_getter(child_id):
            if (isinstance(child_id, Widget) and 
                isinstance(child_args, dict)
            ):
                child_id = child_id._name
            try:
                return child_args[child_id]
            except (IndexError, KeyError, TypeError):
                return {}
        return args_getter
    
    @staticmethod
    def _child_displayer(children, value_for, args_for):
        def display_child(widget, **kw):
            if isinstance(widget, (basestring, int)):
                widget = children[widget]
            child_kw = args_for(widget)
            child_kw.update(kw)
            return widget.display(value_for(widget), **child_kw)
        return display_child

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

    @only_if_uninitialized
    def _append_child(self, obj):
        """Append an object as a child"""

        if obj is None:
            return

        if isinstance(obj, Widget):
            self.children.append(obj)
            obj.parent = self

        elif isinstance(obj, list):
            [self._append_child(o) for o in obj]

        elif isinstance(obj, dict):
            [self._append_child(o) for n, o in obj.iteritems()]

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
              (other.children == self.children)
            )

    def __repr__(self):
        name = self.__class__.__name__
        return "%s(%r)" % (name, self._name)


class InputWidget(Widget):

    params = {
        'strip_name': "If this flag is True then "\
                      "the name of this widget will not be included in the "\
                      "fully-qualified names of the widgets in this subtree. "\
                      "This is useful to 'flatten-out' nested structures. "\
                      "This parameter can only be set during initialization.",
        'required': "Whether the field value is required.",
        'readonly': "Whether the field is readonly.",
        'disabled': "Whether the field is disabled.",
    }

    validator = DefaultValidator

    strip_name = False
    required = False
    readonly = False
    disabled = False

    def __init__(self, name=None, parent=None, children=[], **kw):
        super(InputWidget, self).__init__(name=name, parent=parent, children=children, **kw)

    @property
    def is_required(self):
        if self.required:
            return True
        try:
            self.validator.to_python('', None)
        except:
            return True
        return False

    @property
    def is_disabled(self):
        return self.disabled

    @property
    def is_readonly(self):
        return self.readonly

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
            # Does not adjust_value with Schema because it will recursively
            # call from_python on all sub-validators and that will send
            # strings through their update_params methods which expect
            # python values. adjust_value is called just before sending the
            # value to the template, not before.
            try:
                value = validator.from_python(value)
            except Invalid, e:
                # Ignore conversion errors so bad-input is redisplayed
                # properly
                pass
        return value

    def safe_validate(self, value):
        """Tries to coerce the value to python using the validator. If
        validation fails the original value will be returned unmodified."""
        try:
            value = self.validate(value, use_request_local=False)
        except Exception:
            pass
        return value

    @property
    def children_deep(self):
        out = []
        for c in self.children:
            if getattr(c, 'strip_name', False):
                out += c.children_deep
            else:
                out.append(c)
        return out

    def prepare_dict(self, value, d):
        """
        Prepares the dict sent to the template with functions to access the
        children's errors if any.
        """
        if value is None:
            value = self.get_default()

        error = getattr(cherrypy.request, 'validation_exception', None)

        if error:
            value = getattr(cherrypy.request, 'validation_value', None)
            if self.is_root:
                d['error'] = d.setdefault('error', error)
            else:
                d['error'] = d.setdefault('error', error.error_dict.get(self._name, None))
                value = value.get(self._name, None)
        else:
            d['error'] = d.setdefault('error', None)

        if not isinstance(self.validator, (ForEach,Schema)):
            # Need to coerce value in case the form is being redisplayed with 
            # uncoereced value so update_params always deals with python
            # values. Skip this step if validator will recursively validate
            # because that step will be handled by child widgets.
            value = self.safe_validate(value)
        
        # Propagate values to grand-children with a name stripping parent
        for c in self.children:
            if getattr(c, 'strip_name', False):
                for subc in c.children_deep:
                    if hasattr(subc, '_name'):
                        try:
                            v = value.pop(subc._name)
                        except KeyError:
                            pass
                        else:
                            value.setdefault(c._name, {})[subc._name] = v

        d['error_for'] = self._get_child_error_getter(d['error'])
        
        d = super(InputWidget, self).prepare_dict(value, d)

        d['field_for'] = _field_getter(self.c)
        # Adjust the value with the validator if present and the form is not
        # being redisplayed because of errors *just before* sending  it to the
        # template.
        if not error:
            d['value'] = self.adjust_value(d['value'])
            # Rebind these getters with the adjusted value
            d['value_for'] = self._get_child_value_getter(d.get('value'))
            # Provide a shortcut to display a child field in the template
            d['display_child'] = self._child_displayer(self.children,
                                                        d['value_for'],
                                                        d['args_for'])
        return d

    def update_params(self, d):
        super(InputWidget, self).update_params(d)

        if not self.strip_name and self.is_required:
            d.css_classes.append('requiredfield')
        if not self.strip_name and  self.is_readonly:
            d.css_classes.append('readonlyfield')
        if  not self.strip_name and self.is_disabled:
            d.css_classes.append('disabledfield')

        if d.error:
            d.css_classes.append("has_error")

    def _get_child_error_getter(self, error):
        def error_getter(child_id):
            try:
                if error and error.error_dict:
                    if isinstance(child_id, Widget):
                        child_id = child_id._name
                    return error.error_dict[child_id]
            except (IndexError, KeyError): pass
            return None
        return error_getter


def _field_getter(children):
    return lambda name: children[name]

