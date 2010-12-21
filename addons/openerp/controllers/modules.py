import os
import shutil
import tempfile
import zipfile
from cStringIO import StringIO

from openerp.controllers import form
from openerp.utils import rpc

from openobject import paths, addons
from openobject.tools import zip

class ModuleForm(form.Form):
    _cp_path = "/openerp/modules"

    def has_new_modules(self):
        """ Returns whether there are new web modules available for download
        (brand new or updates)

        :rtype bool:
        """
        return bool([
            name for (name, version) in rpc.RPCProxy('ir.module.module').list_web()
            if (not addons.exists(name)
                or version > addons.get_info(name).get('version', '0'))
        ])

    def get_new_modules(self):
        if not addons.writeable: return []
        modules = rpc.RPCProxy('ir.module.module')
        web_modules = modules.list_web()
        if not web_modules: return []

        addons_to_download = [
            name for (name, version) in web_modules
            if (not addons.exists(name)
                or version > addons.get_info(name).get('version', '0'))
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
                'version': module['version'].encode('utf-8'),
                # addons depend at least of openerp
                'depends': dependencies or ['openerp'],
            },))
            descriptor.close()
        return addons_to_download
