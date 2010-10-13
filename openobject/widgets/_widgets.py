import re

from _base import *
from _resource import *
from _utils import make_bunch

import formencode


def name2label(name):
    """
    Convert a column name to a Human Readable name.

    Yanked from TGFastData
    """
    # Create label from the name:
    #   1) Convert _ to spaces
    #   2) Convert CamelCase to Camel Case
    #   3) Upcase first character of Each Word
    # Note: I *think* it would be thread-safe to
    #       memoize this thing.
    return ' '.join([s.capitalize() for s in
               re.findall(r'([A-Z][a-z0-9]+|[a-z0-9]+|[A-Z0-9]+)', name)])


class FormField(InputWidget):
    """
    Base class for all Widgets that can be attached to a Form or FieldSet.

    Form and FieldSets are in turn FormFields so they can be arbitrarily nested.
    These widgets can provide a validator that should validate and coerce the
    input they generate when submitted.
    """

    params = {
        'label_text': 'The text to label the field',
        'help_text': 'Description of the field',
        'field_id': 'Identifier of the field, the id attribute',
        'attrs': 'Extra attributes for the outermost DOM node',
    }

    attrs = {}
    file_upload = False

    def __init__(self, name=None, **params):
        super(FormField, self).__init__(name, **params)
        if self.label_text is None and self.name is not None:
            pos = self.name.rfind('.')
            name = self.name[pos+1:]
            self.label_text = name2label(name)

        self.attrs = make_bunch(self.attrs or {})

    def update_params(self, d):
        super(FormField, self).update_params(d)

    def update_attrs(self, d, *args, **kw):

        for arg in args:
            if isinstance(arg, dict):
                d.attrs.update(arg)
            else:
                d.attrs[arg] = d[arg]

        for name, value in kw.items():
            d.attrs[name] = value


class Label(FormField):
    """A simple label for a form field."""

    template = """
    <label id="${field_id}" class="${css_class}" ${py.attrs(attrs)}>${value}</label>"
    """


class Input(FormField):
    """A standard, form input field."""

    template = """\
    <input type="${type}" ${py.attrs(attrs)} class="${css_class}"/>
    """

    params = {
        'type': 'Input type',
    }

    type = "text"

    def update_params(self, d):
        super(Input, self).update_params(d)
        d.field_id = self.full_name.replace('.', '_')
        self.update_attrs(d, "name", "value", id=d.field_id, title=self.help_text)


class TextField(Input):
    params = {
        'size': 'The size of the field',
        'maxlength': 'Maximum size of the field',
    }

    def update_params(self,d):
        super(TextField, self).update_params(d)
        self.update_attrs(d, 'size', 'maxlength')


class PasswordField(Input):
    type = "password"


class HiddenField(Input):
    type = "hidden"


class FileField(Input):
    type = "file"
    file_upload = True

class Button(Input):
    type = "button"


class SubmitButton(Input):
    type = "submit"


class ResetButton(Input):
    type = "reset"


class ImageButton(Input):
    type = "image"
    params = {'src': 'Source of the image',
              'width': 'Width of the image',
              'height': 'Height of the image',
              'alt': 'Alternate text for the image'}

    def update_params(self, d):
        super(ImageButton, self).update_params(d)
        self.update_params(d, "width", "height", "src", "alt")


class CheckBox(Input):
    type = "checkbox"
    validator = formencode.validators.Bool
    def update_params(self, d):
        super(CheckBox, self).update_params(d)
        try:
            checked = self.validator.to_python(d.value)
        except formencode.api.Invalid:
            checked = False
        d.attrs['checked'] = checked or None


class RadioButton(Input):
    type = "radio"


class TextArea(Input):

    template = """\
    <textarea ${py.attrs(attrs)} class="${css_class}"
        rows="${rows}" cols="${cols}">${value}</textarea>
    """

    params = {'rows': 'Number of rows to render',
              'cols' : 'Number of columns to render'}
    rows = 7
    cols = 50


class SelectField(Input):

    template = """\
    <select ${py.attrs(attrs)} class="${css_class}">
    % for group, options in grouped_options:
    % if group:
    <optgroup label="${group}">
    % endif
        % for val, desc, _attrs in options:
        <option value="${val}" ${py.attrs(_attrs)}>${desc}</option>
        % endfor
    % if group:
    </optgroup>
    % endif
    % endfor
    </select>
    """

    params = {
        'options': 'A list of tuples with the options for the select field',
        'multiple': 'Whether it is a multi select box',
    }
    options = []

    def _iterate_options(self, options):
        for option in options:
            if not isinstance(option, (tuple,list)):
                yield (option, option)
            else:
                yield option

    def _is_option_selected(self, option_value, value):
        if self.multiple:
            return value is not None and option_value in value
        return option_value == value

    def update_params(self, d):
        super(SelectField, self).update_params(d)
        grouped_options = []
        options = []
        d['options'] = self._iterate_options(d['options'])
        # Coerce value if possible so _is_options_selected can compare python
        # values. This is needed when validation fails because FE will send
        # uncoerced values.
        value = self.safe_validate(d['value'])
        for optgroup in d["options"]:
            if isinstance(optgroup[1], (list,tuple)):
                group = True
                optlist = optgroup[1][:]
            else:
                group = False
                optlist = [optgroup]
            for i, option in enumerate(self._iterate_options(optlist)):
                if len(option) is 2:
                    option_attrs = {}
                elif len(option) is 3:
                    option_attrs = dict(option[2])
                if self._is_option_selected(option[0], value):
                    option_attrs['selected'] = 'selected'
                optlist[i] = (option[0], option[1], option_attrs)
            options.extend(optlist)
            if group:
                grouped_options.append((optgroup[0], optlist))
        # options provides a list of *flat* options leaving out any eventual
        # group, useful for backward compatibility and simpler widgets
        d["options"] = options
        if grouped_options:
            d["grouped_options"] = grouped_options
        else:
            d["grouped_options"] = [(None, options)]

        if self.multiple:
            d.attrs.multiple = "multiple"

class Form(FormField):

    template = """\
    <form ${py.attrs(attrs)} class="${css_class}">
        % if hidden_fields:
        <div>
            % for child in hidden_fields:
            ${display_member(child)}
            % endfor
        </div>
        % endif
        <table class="form-container">
            % for child in fields:
            <%
                error = error_for(child)
                label = label_for(child)
            %>
            <tr>
                <td class="label">
                    <label id="${child.name}.label" for="${child.name}" class="fieldlabel">${label}</label>
                </td>
                <td class="fieldcol">
                    ${display_member(child)}
                    % if error:
                    <span class="fielderror">${error}</span>
                    % endif
                </td>
            </tr>
            % endfor
            <tr>
                <td>&nbsp;</td>
                <td align="right" style="padding: 0px 5px 5px 0px;"><button type="submit" class="static_boxes">${submit_text}</button></td>
            </tr>
        </table>
    </form>
    """

    params = ['action', 'method', 'submit_text']
    member_widgets = ['hidden_fields', 'fields']

    hidden_fields = []
    fields = []

    method = "POST"
    submit_text = "Submit"
    form_attrs = {}
    form = True

    def __init__(self, name=None, **params):
        super(Form, self).__init__(name, **params)

    def label_for(self, field):
        return getattr(field, "label", None) or getattr(field, "_name", None)

    def update_params(self, d):
        super(Form, self).update_params(d)

        d['label_for'] = self.label_for
        self.update_attrs(d, self.form_attrs)
        self.update_attrs(d, "name", "action", "method", id=self.name)

        if self.file_upload:
            self.attrs.setdefault('enctype', 'multipart/form-data')

    @property
    def file_upload(self):
        for field in self.iter_member_widgets():
            if getattr(field, 'file_upload', False):
                return True
        return False
