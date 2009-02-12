import os, sys

# ubuntu 8.04 has obsoleted `pyxml` package and installs here.
# the path needs to be updated before any `import xml`
_oldxml = '/usr/lib/python%s/site-packages/oldxml' % sys.version[:3]
if os.path.exists(_oldxml):
    sys.path.append(_oldxml)

# Check for PyXML as it's not compatible with pkg_resources on some systems
try:
    exec("import xml.xpath")
except ImportError:
    print 'Error: python-xml >= 0.8.4 (PyXML, XML Tools for python) is required.'
    sys.exit(1)

from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

execfile(os.path.join("openerp", "release.py"))

if 'bdist_rpm' not in sys.argv:
    version = version + '-' + release

# Provided as an attribute, so you can append to these instead
# of replicating them:
standard_exclude = ('*.py', '*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build',
                                './dist', 'EGG-INFO', '*.egg-info')
def find_package_data(
    where='.', package='',
    exclude=standard_exclude,
    exclude_directories=standard_exclude_directories,
    only_in_packages=True,
    show_ignored=False):
    """
    Return a dictionary suitable for use in ``package_data``
    in a distutils ``setup.py`` file.

    The dictionary looks like::

        {'package': [files]}

    Where ``files`` is a list of all the files in that package that
    don't match anything in ``exclude``.

    If ``only_in_packages`` is true, then top-level directories that
    are not packages won't be included (but directories under packages
    will).

    Directories matching any pattern in ``exclude_directories`` will
    be ignored; by default directories with leading ``.``, ``CVS``,
    and ``_darcs`` will be ignored.

    If ``show_ignored`` is true, then all the files that aren't
    included in package data are shown on stderr (for debugging
    purposes).

    Note patterns use wildcards, or can be exact paths (including
    leading ``./``), and all searching is case-insensitive.
    """

    out = {}
    stack = [(convert_path(where), '', package, only_in_packages)]
    while stack:
        where, prefix, package, only_in_packages = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print >> sys.stderr, (
                                "Directory %s ignored by pattern %s"
                                % (fn, pattern))
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                    stack.append((fn, '', new_package, False))
                else:
                    stack.append((fn, prefix + name + '/', package, only_in_packages))
            elif package or not only_in_packages:
                # is a file
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print >> sys.stderr, (
                                "File %s ignored by pattern %s"
                                % (fn, pattern))
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

packages = find_packages()
package_data = find_package_data(where='openerp', package='openerp')

if os.path.isdir('locales'):
    packages.append('locales')
    package_data.update(find_package_data(where='locales', exclude=('*.po',), only_in_packages=False))

data_files = []
for name in ('config', 'scripts', 'doc'):
    data = find_package_data(where=name, package=name, exclude=('*~',), only_in_packages=False)
    data_files += [(name, [name + '/' + f for f in data[name]])]

setup(
    name = "openerp-web",
    version = version,
    description = description,
    long_description = long_description,
    author = author,
    author_email = email,
    url = url,
    download_url = download_url,
    copyright = copyright,
    license = license,

    install_requires=[
        "TurboGears >= 1.0.7, < 1.1b1",
        "pyparsing >= 1.5.0"
    ],

    zip_safe = False,
    packages = packages,
    package_data = package_data,
    keywords = [
        # Use keywords if you'll be adding your package to the
        # Python Cheeseshop
        'turbogears.app',
    ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: TurboGears',
        'Framework :: TurboGears :: Applications',
        ],
    test_suite = 'nose.collector',
    entry_points = {
        'console_scripts': [
            'start-openerp-web = openerp.commands:start',
        ],
    },

    data_files = data_files,
    )

# vim: ts=4 sts=4 sw=4 si et

