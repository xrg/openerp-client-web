from openerp.controllers import form
from openerp.utils import rpc, TinyDict

from openobject.tools import expose


class ModuleForm(form.Form):

    _cp_path = "/openerp/modules"

    @expose(template="templates/modules.mako")
    def create(self, params, tg_errors=None):
        params.model = "ir.module.web"
        params.view_type = "tree"
        params.view_mode = "['tree']"
        params.ids = None
        params.editable = False

        params.context = ctx = rpc.session.context.copy()
        ctx['reload'] = True

        form = self.create_form(params, tg_errors)
        return dict(form=form, params=params)

    @expose()
    def index(self):

        from openobject import addons

        modules = addons.get_module_list()
        data = []

        for name in modules:
            mod = addons.get_info(name)

            mod['module'] = name

            mod.pop("depends", None)
            mod.pop("version", None)
            if mod.pop("active", False):
                mod["state"] = "uninstallable"

            data.append(mod)

        proxy = rpc.RPCProxy("ir.module.web")
        proxy.update_module_list(data)

        params = TinyDict()
        return self.create(params)

    def get_installed_modules(self):

        proxy = rpc.RPCProxy("ir.module.web")
        ids = proxy.search([('state', '=', 'installed')])

        return [m['module'] for m in proxy.read(ids)]
