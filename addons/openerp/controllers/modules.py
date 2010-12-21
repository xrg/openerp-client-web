import os
import shutil
import tempfile
import zipfile
from cStringIO import StringIO

from openerp.controllers import form
from openerp.utils import rpc, TinyDict

from openobject import paths, addons
from openobject.tools import expose, zip

class ModuleForm(form.Form):
    _cp_path = "/openerp/modules"

    @expose(template="/openerp/controllers/templates/modules.mako")
    def index(self):
        modules = addons.get_local_addons()
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
        params.model = "ir.module.web"
        params.view_type = "tree"
        params.view_mode = "['tree']"
        params.ids = None
        params.editable = False

        params.context = ctx = rpc.session.context.copy()
        ctx['reload'] = True

        form = self.create_form(params)
        return dict(form=form, params=params)

    def get_new_modules(self):
        modules = rpc.RPCProxy('ir.module.module')
        web_modules = [module[0] if isinstance(module, (tuple,list)) else module
                       for module in modules.list_web()]
        if not web_modules: return []

        addons_to_download = [
            module for module in web_modules
            if not os.path.isdir(paths.addons(module))
        ]
        # avoid querying for 0 addons if we have everything already
        if not addons_to_download: return []
        web_payload = modules.get_web(addons_to_download)
        for module in web_payload:
            # Due to the way zip_directory works on the server, we get a toplevel dir called "web" for our addon,
            # rather than having it named "the right way". Dump to temp directory and move to right name.
            temp_dir = tempfile.mkdtemp()
            module_content = zipfile.ZipFile(StringIO(module['content'].decode('base64')))
            zip.extractall(module_content, temp_dir)
            module_content.close()

            # cleanup any existing addon of the same name
            module_dir = paths.addons(module['name'])
            shutil.rmtree(module_dir, ignore_errors=True)

            shutil.move(os.path.join(temp_dir, 'web'), module_dir)
            shutil.rmtree(temp_dir)

            dependencies = map(lambda u: u.encode('utf-8'), module['depends'])
            descriptor = open(os.path.join(module_dir, '__openerp__.py'), 'wb')
            descriptor.write('# -*- coding: utf-8 -*-\n')
            descriptor.write("%s" % ({
                'name': module['name'].encode('utf-8'),
                # addons depend at least of openerp
                'depends': dependencies or ['openerp'],
            },))
            descriptor.close()
        return web_modules
