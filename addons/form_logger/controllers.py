from openobject.tools import expose
from openerp.controllers import form

class Form(form.Form):
    _cp_path = "/openerp/form"
    @expose(mark_only=True)
    def edit(self, *args, **kwargs):
        return super(Form, self).edit(*args, **kwargs)
