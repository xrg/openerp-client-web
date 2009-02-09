###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# The OpenERP web client is distributed under the "OpenERP Public License".
# It's based on Mozilla Public License Version (MPL) 1.1 with following 
# restrictions:
#
# -   All names, links and logos of Tiny, Open ERP and Axelor must be 
#     kept as in original distribution without any changes in all software 
#     screens, especially in start-up page and the software header, even if 
#     the application source code has been changed or updated or code has been 
#     added.
#
# -   All distributions of the software must keep source code with OEPL.
# 
# -   All integrations to any other software must keep source code with OEPL.
#
# If you need commercial licence to remove this kind of restriction please
# contact us.
#
# You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################

import turbogears as tg
import cherrypy

from openerp import tools

def eval_get(attrs, name, default=None):
    if name not in attrs:
        return default

    val = attrs[name]
    if isinstance(val, basestring):
        val = val.title()

    return tools.expr_eval(val)

class TinyWidget(object):
    """Widget interface, every widget class should implement
    this class.
    """

    colspan = 1
    rowspan = 1
    string = None
    nolabel = False
    select = False
    required = False
    readonly = False
    help = None
    editable = True
    translatable = False
    visible = True
    inline = False

    name = None
    model = None
    states = None
    callback = None
    change_default = None
    onchange = 'onChange(this)'
    kind=None
    
    field_class = None

    def __init__(self, attrs={}):
        self.string = attrs.get("string", None)
        self.model = attrs.get("model", None)

        prefix = attrs.get('prefix', '')
        self.name = prefix + (prefix and '/' or '') + attrs.get('name', '')

        self.states = attrs.get('states', None)
        if isinstance(self.states, basestring):
            self.states = self.states.split(',')

        self.colspan = int(attrs.get('colspan', 1))
        self.rowspan = int(attrs.get('rowspan', 1))
        
        self.select = eval_get(attrs, 'select', False)
        self.nolabel = eval_get(attrs, 'nolabel', False)
        self.required = eval_get(attrs, 'required', False)
        self.readonly = eval_get(attrs, 'readonly', False)
        self.visible = True
        self.inline = attrs.get('inline');
        
        try:
            visval = attrs.get('invisible', 'False')
            ctx = attrs.get('context', {})
            self.invisible = eval(visval, {'context': ctx})
        except:
            pass
        
        self.help = attrs.get('help')
        self.editable = attrs.get('editable', True)
        self.translatable = attrs.get('translate', False)

        self.set_state(attrs.get('state', 'draft'))

        self.callback = attrs.get('on_change', None)
        self.change_default = attrs.get('change_default', False)
        self.kind = attrs.get('type', None)

        self.attributes = attrs.get('attrs', {})

    def set_state(self, state):

        if isinstance(self.states, dict) and state in self.states:

            attrs = dict(self.states[state])

            if 'readonly' in attrs:
                self.readonly = attrs['readonly']

            if 'required' in attrs:
                self.required = attrs['required']

            if 'value' in attrs:
                self.default = attrs['value']

class TinyInputWidget(TinyWidget):
    """Interface for Field widgets, every InputField widget should
    implement this class
    """

    def __init__(self, attrs={}):
        TinyWidget.__init__(self, attrs)
        self._validator = None

    def get_validator(self):

        # required fields are now validated at client side
        #if self._validator:
        #    self._validator.not_empty = (self.required or False) and True
        #elif self.required:
        #    self._validator = tg.validators.NotEmpty()

        return self._validator

    def set_validator(self, value):
        self._validator = value

    validator = property(get_validator, set_validator)

    def get_value(self):
        """Get the value of the field.

        @return: field value
        """
        return self.default

    def set_value(self, value):
        """Set the value of the field.

        @param value: the value
        """
        if isinstance(value, basestring):
            value = ustr(value)

        self.default = value
        
    def get_display_value(self):
        """Get the display value of the field.
        """
        
        try:
            return self.validator.from_python(self.default)
        except:
            pass
        
        return self.get_value()
    
    def update_params(self, d):
        super(TinyInputWidget, self).update_params(d)

        attrs = d['attrs'] = {}

        attrs['change_default'] = self.change_default or None
        attrs['callback'] = self.callback or None
        attrs['onchange'] = self.onchange

        # name as field_id
        d['field_id'] = self.name
        d['kind'] = self.kind
        d['editable'] = self.editable
        d['inline'] = self.inline

        if self.readonly:
            d['field_class'] = " ".join([d['field_class'], "readonlyfield"])
            attrs['disabled'] = 'disabled'

        if self.required and 'requiredfield' not in d['field_class'].split(' '):
            d['field_class'] = " ".join([d['field_class'], "requiredfield"])

        if self.translatable and 'translatable' not in d['field_class'].split(' '):
            d['field_class'] = " ".join([d['field_class'], "translatable"])

        if hasattr(self, 'error') and self.error:
            d['field_class'] = " ".join([d['field_class'], "errorfield"])

class TinyCompoundWidget(TinyInputWidget, tg.widgets.CompoundWidget):

    def __init__(self, attrs={}):
        TinyInputWidget.__init__(self, attrs)
        tg.widgets.CompoundWidget.__init__(self, name=self.name or None)

    def get_widgets_by_name(self, name, kind=tg.widgets.Widget, parent=None):
        result = []
        parent = parent or self

        for wid in parent.iter_member_widgets():

            if wid.name == name and isinstance(wid, kind):
                result.append(wid)

            if isinstance(wid, tg.widgets.CompoundWidget):
                result += self.get_widgets_by_name(name, kind=kind, parent=wid)

        return result

    def get_last_update_info(resource, values):
        result = {}
        for item in values:
            result["%s,%s" % (resource, item['id'])] = item.pop('__last_update', '')
        return result

    def _update_concurrency_info(self, resource, records):
        info = getattr(cherrypy.request, 'terp_concurrency_info', {})
        vals = info.setdefault(resource, {})
        for item in records:
            vals[item['id']] = item.pop('__last_update', '')
        cherrypy.request.terp_concurrency_info = info

    def update_params(self, d):
        tg.widgets.CompoundWidget.update_params(self, d)
        d['editable'] = self.editable
        
class TinyField(TinyInputWidget, tg.widgets.FormField):

    def __init__(self, attrs):
        TinyInputWidget.__init__(self, attrs)
        tg.widgets.FormField.__init__(self, name=self.name)

class ConcurrencyInfo(TinyCompoundWidget):
    template="""<span xmlns:py="http://purl.org/kid/ns#" py:strip="" py:if="ids and model in info">
        <input type="hidden" py:if="id in info[model]" py:for="id in ids"
            name="_terp_concurrency_info" value="('$model,$id', '${info[model][id]}')"/>
    </span>"""

    params = ['ids', 'model', 'info']

    def __init__(self, model, ids):
        self.ids = ids
        self.model = model

    def _get_concurrency_info(self):
        return getattr(cherrypy.request, 'terp_concurrency_info', {})

    info = property(_get_concurrency_info)

# vim: ts=4 sts=4 sw=4 si et


