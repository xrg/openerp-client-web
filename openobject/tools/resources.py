import os
import fnmatch

__all__ = ['find_resource', 'find_resources']

def find_resource(package_or_module, *names):

    ref = package_or_module
    if isinstance(package_or_module, basestring):
        ref = __import__(package_or_module, globals(), locals(), \
                package_or_module.split('.'))

    return os.path.abspath(os.path.join(os.path.dirname(ref.__file__), *names))


def find_resources(package_or_module, path=None, patterns=None):

    root = find_resource("openobject")
    path = path or ""
    patterns = patterns or []

    if path:
        root = os.path.join(root, path)

    for path, dirs, files in os.walk(os.path.abspath(root)):
        for pattern in patterns:
            for filename in fnmatch.filter(files, pattern):
                yield os.path.join(path, filename)
