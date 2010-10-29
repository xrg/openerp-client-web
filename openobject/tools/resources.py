import os
import fnmatch

import pkg_resources

__all__ = ['resource_exists', 'find_resource', 'find_resources']

def resource_exists(package_or_module, *names):
    return pkg_resources.resource_exists(
        package_or_module, os.path.join(*names)
    )

def find_resource(package_or_module, *names):
    return pkg_resources.resource_filename(
            package_or_module, os.path.join(*names))

def find_resources(package_or_module, path=None, patterns=None):
    try:
        root = find_resource("openobject", '')
        path = path or ""
        patterns = patterns or []

        if path:
            root = os.path.join(root, path)

        for path, dirs, files in os.walk(os.path.abspath(root)):
            for pattern in patterns:
                for filename in fnmatch.filter(files, pattern):
                    yield os.path.join(path, filename)
    except:
        # blew up because we're inside a zip, only used for mako
        # template reloading anyway so who cares
        return
