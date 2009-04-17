
from base import *
from resource import *

from openerp.validators import *

class FormField(Widget):
    
    params = {
        'label': 'Label of the field.',
        'help': 'Help text',
        'field_id': 'field id',
        'attrs': 'Dictionary containing extra attributes for the field.'
    }
    
    attrs = {}
    
    @property
    def field_id(self):
        name = self.name
        if name:
            return name.replace('.', '_')
        return name
    
    def __init__(self, name=None, label=None, help=None, **kw):
        super(FormField, self).__init__(name=name, label=label, help=help, **kw)       

class Label(FormField):
    """A simple label for a form field."""
    
    template = """
    <label id="${field_id}" class="${css_class}" ${py.attrs(attrs)}>${value}</label>"
    """


class Input(FormField):
    """A standard, form input field."""
     
    template = """\
    <input type="${type}" ${py.attrs(attrs)}/>
    """
    
    params = {
        'type': 'Input type',
    }
    
    type = "text"
    
    def update_params(self, d):
        super(Input, self).update_params(d)
        attrs = d.setdefault('attrs', {})
        attrs.update(self.attrs)
        if self.field_id:
            attrs['id'] = self.field_id
        if self.name:
            attrs['name'] = self.name
        if self.help:
            attrs['title'] = self.help
        if self.css_class:
            attrs['class'] = self.css_class
            
        attrs['value'] = d['value']
            
class TextField(Input):
    pass

class PasswordField(Input):
    type = "password"
    
class HiddenField(Input):
    type = "hidden"
    
class FileField(Input):
    type = "file"
    
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
        attrs = d.setdefault('attrs', {})
        attrs['width'] = self.width
        attrs['height'] = self.height
        attrs['src'] = self.src
        attrs['alt'] = self.alt

class CheckBox(Input):
    type = "checkbox"
    
    def update_params(self, d):
        super(CheckBox, self).update_params(d)
        if d['value']:
            d['attrs']['checked'] = 'checked'
            
class TextArea(Input):
    
    template = """\
    <textarea ${py.attrs(attrs) rows="${rows}" cols="${cols}">${value}</textarea>
    """
    
    params = {'rows': 'Number of rows to render',
              'cols' : 'Number of columns to render'}
    rows = 7
    cols = 50


class SelectField(Input):
    
    template = """\
    <select ${py.attrs(attrs)}>
    % for group, opts in grouped_options:
        % if group:
    <optgroup label="${group}">
        % endif
        % for val, text in opts:
            <option value="${val}" ${py.selector(val==value)}>${text}</option>
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
    
    def _get_options(self, options):
        
        result = []
        
        for opt in options:
            
            if not isinstance(opt, (list, tuple)):
                result.append([None, [(opt, opt)]])
            
            elif len(opt) == 2 and isinstance(opt[1][1], (list, tuple)):
                result.append(opt)
                
            elif len(opt) == 2:
                result.append([None, [opt]])
        
        return result
    
    
    def update_params(self, d):
        super(SelectField, self).update_params(d)
        if callable(self.options):
            d['options'] = self.options()
        d['grouped_options'] = self._get_options(d['options'])
        if self.multiple:
            d['attrs']['multiple'] = "multiple"
    
class Form(FormField):
    
    template = """\
    <form ${py.attrs(attrs)}>
        % for child in hidden_fields:
        ${display_child(child)}
        % endfor
        <table border="0">
            % for child in fields:
            <tr>
                <td>${label_for(child)}</td>
                <td>${display_child(child)}</td>
            </tr>
            % endfor
            <tr>
                <td>&nbsp;</td>
                <td><input type="submit" value="${submit_text}"/></td>
            </tr>
        </table>
    </form>
    """

    params = ['action', 'method', 'hidden_fields', 'submit_text']
    members = ['hidden_fields', 'fields']

    hidden_fields = []
    fields = []
    
    method = "POST"
    submit_text = "Submit"
    form_attrs = {}
    
    strip_name = True
    
    def __init__(self, name=None, **kw):
        super(Form, self).__init__(name=name, **kw)
        
    def post_init(self, *args, **kw):
        for name in self.members:
            member = getattr(self, name)
            if isinstance(member, Widget) and member not in self.fields:
                self.fields.append(member)

    def label_for(self, field):
        return getattr(field, "label", None) or getattr(field, "_name", None)
    
    def update_params(self, d):
        super(Form, self).update_params(d)
        d['label_for'] = self.label_for
        attrs = d.setdefault('attrs', {})
        
        attrs['id'] = self.name
        attrs['name'] = self.name
        attrs['action'] = self.action
        attrs['method'] = self.method
        attrs.update(self.form_attrs)
        
