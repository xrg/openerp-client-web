import copy

from itertools import count, chain, ifilterfalse

import cherrypy
import formencode.foreach

import openobject
from openobject import tools
from openobject.validators import *

from _meta import WidgetType
from _utils import OrderedSet, make_bunch


__all__ = ['Widget', 'InputWidget']


_serial_generator = count()

class Widget(object):

    __metaclass__ = WidgetType

    template = None

    css = []
    javascript = []

    css_class = None
    css_classes = []

    params = {
        'name': 'The Name for this Widget.',
        'css_class': 'Main CSS class for this widget',
        'css_classes': 'List of all CSS classes',
    }

    member_widgets = []
    default = None
    parent = None

    def __new__(cls, *args, **kwargs):
        actual_cls = openobject.pooler.get_pool().get(
                cls.widget_key, group='widgets')
        # if there is nothing in the pool yet (uh?)
        return object.__new__(actual_cls or cls)

    def __init__(self, name=None, **params):
        # set each keyword args as attribute
        for k, v in params.iteritems():
            if not k.startswith('_'):
                try:
                    setattr(self, k, v)
                except AttributeError, e:
                    #skip setting the value of a read only property
                    pass

        self._name = name
        self._serial = _serial_generator.next()

        # params & member_widgets
        for name in chain(self.__class__.params, self.__class__.member_widgets):
            try:
                attr = getattr(self, name, None)
                if isinstance(attr, list):
                    attr = copy.copy(attr)
                elif isinstance(attr, dict):
                    attr = attr.copy()
                setattr(self, name, attr)
            except AttributeError, e:
                pass

        self._resources = OrderedSet()

        # Set default css class for the widget
        if not getattr(self, 'css_class', None):
            self.css_class = self.__class__.__name__.lower()

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        item = self
        while item:
            yield item
            item = item.parent

    @property
    def root(self):
        return list(self.path)[-1]

    @property
    def is_root(self):
        return self.parent is None

    def adjust_value(self, value, **params):
        """Adjust the value sent to the template on display."""
        if value is None:
            value = self.default
            if callable(value):
                value = value()
        return value

    def iter_member_widgets(self):
        """Iterates over all the widget's children
        """
        for member in self.__class__.member_widgets:
            attr = getattr(self, member, None)
            if isinstance(attr, list):
                for widget in attr:
                    yield widget
            elif isinstance(attr, dict):
                for name, widget in attr.iteritems():
                    yield widget
            elif attr is not None:
                yield attr

    def value_for(self, item, value):
        """
        Get value for member widget.

        Pick up the value for a given member_widget 'item' from the
        value dict passed to this widget.
        """

        if getattr(item, 'strip_name', False):
            return value

        name = getattr(item, "name", item)
        if isinstance(value, dict):
            return value.get(name)
        else:
            return None

    def params_for(self, item, **params):
        """
        Get params for member widget.

        Pick up the params for the given member_widget 'item' from
        the params dict passed to this widget.
        """

        if getattr(item, 'strip_name', False):
            return params

        name = getattr(item, "name", item)
        item_params = {}
        for k, v in params.iteritems():
            if isinstance(v, dict):
                if name in v:
                    item_params[k] = v[name]
        return item_params

    def display_member(self, item, value, **params):

        if isinstance(item, basestring):
            item = getattr(self, item, None)

        assert isinstance(item, Widget), "Invalid member widget."

        v = self.value_for(item, value)
        d = self.params_for(item, **params)
        return item.display(v, **d)

    def update_params(self, params):

        # Populate dict with attrs from self listed at params and member_widgets
        for k in ifilterfalse(params.__contains__, chain(self.params, self.member_widgets)):
            attr = getattr(self, k, None)
            if attr is not None:
                if not isinstance(attr, Widget) and callable(attr):
                    attr = attr()
            params[k] = attr

        for w in self.iter_member_widgets():
            w.parent = self

        v = params['value']
        d = params['member_widgets_params']

        params.update(
            value_for=lambda f: self.value_for(f, v),
            params_for=lambda f: self.params_for(f, **d),
            display_member=lambda f: self.display_member(f, v, **d))

        params.css_class = ' '.join(set([params['css_class'] or ''] + params['css_classes']))

    def display(self, value=None, **params):

        params['member_widgets_params'] = params.copy()

        d = make_bunch(params)
        d.value = self.adjust_value(value, **params)

        self.update_params(d)

        d['css_class'] = ' '.join(set([d['css_class'] or ''] + d['css_classes']))

        return tools.render_template(
                tools.load_template(
                    self.template), d)

    def render(self, value=None, **params):
        return self.display(value, **params)

    def retrieve_css(self):
        """
        Return the needed CSS ressources.

        Return a setlike instance with all the CSSLinks and CSSSources
        the widget needs.
        """
        css = OrderedSet()
        for cssitem in self.css:
            css.add(cssitem)
        for widget in self.iter_member_widgets():
            for cssitem in widget.retrieve_css():
                css.add(cssitem)
        return css

    def retrieve_javascript(self):
        """
        Get JavaScript for the member widgets.

        Retrieve the JavaScript for all the member widgets and
        get an ordered union of them.
        """
        scripts = OrderedSet()
        for script in self.javascript:
            scripts.add(script)
        for widget in self.iter_member_widgets():
            for script in widget.retrieve_javascript():
                scripts.add(script)
        return scripts

    def __ne__(self, other):
        return not (self == other)

    def __eq__(self, other):
        return (
              (type(other) is type(self)) and
              (other._serial == self._serial) and
              (other._name == self._name)
            )

    def __repr__(self):
        return self.__class__.__name__


class InputWidget(Widget):

    params = {
        'required': "Whether the field value is required.",
        'readonly': "Whether the field is readonly.",
        'disabled': "Whether the field is disabled.",
    }

    validator = DefaultValidator

    required = False
    readonly = False
    disabled = False

    strip_name = False

    def __init__(self, name=None, **params):
        super(InputWidget, self).__init__(name, **params)

    @property
    def full_name(self):
        return ".".join(reversed([w.name for w in self.path if w.name and not getattr(w, 'strip_name', False)]))

    @property
    def is_validated(self):
        try:
            if self.root is cherrypy.request.validated_form:
                return True

            for w in cherrypy.request.validated_form.iter_member_widgets():
                if w is self.root:
                    return True
        except:
            pass
        return False

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
            return self.validator.to_python(value, state)
        return value

    def safe_validate(self, value):
        """Tries to coerce the value to python using the validator. If
        validation fails the original value will be returned unmodified."""

        # don't validate empty values
        if value is None or (isinstance(value, basestring) and value.strip() == ""):
            return value

        try:
            return self.validate(value)
        except Exception:
            pass
        return value

    def adjust_value(self, value, **params):
        """Adjusts the python value sent to :meth:`Widget.display` with
        the validator so it can be rendered in the template.
        """

        iv = None
        if hasattr(cherrypy.request, 'input_values') and self.is_validated:
            iv = cherrypy.request.input_values.get(self._name)

        if iv is not None and not isinstance(self.validator, (formencode.foreach.ForEach, Schema)):
            value = self.safe_validate(iv)
        else:
            value = super(InputWidget, self).adjust_value(value, **params)

        if self.validator and not isinstance(self.validator, Schema):
            # Does not adjust_value with Schema because it will recursively
            # call from_python on all sub-validators and that will send
            # strings through their update_params methods which expect
            # python values. adjust_value is called just before sending the
            # value to the template, not before.
            try:
                return self.validator.from_python(value)
            except Exception:
                # Ignore conversion errors so bad-input is redisplayed properly
                pass
        return value

    def update_params(self, params):

        if self.is_validated:
            error = getattr(cherrypy.request, 'validation_exception', None)

            if self.is_root:
                params['error'] = params.setdefault('error', error)
            elif error:
                params['error'] = params.setdefault('error', error.error_dict.get(self._name, None))
        else:
            params['error'] = params.setdefault('error', None)

        super(InputWidget, self).update_params(params)

        classes = set(params.css_classes)
        if not self.strip_name:

            if self.is_required:
                classes.add('requiredfield')

            if self.is_readonly:
                classes.add('readonlyfield')

            if self.is_disabled:
                classes.add('disabledfield')

            if getattr(params, 'error', None):
                classes.add('errorfield')
        params.css_classes = list(classes)

        params['error_for'] = lambda f: self.error_for(f, params['error'])

    def error_for(self, item, error):

        if getattr(item, "strip_name", False):
            return error

        try:
            return error.error_dict[item.name]
        except:
            pass
        return None
