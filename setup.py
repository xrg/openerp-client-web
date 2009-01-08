from setuptools import setup, find_packages
from turbogears.finddata import find_package_data

import os
execfile(os.path.join("openerp", "release.py"))

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
        "TurboGears >= 1.0.7, < 1.1",
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
        'Development Status :: 4 - Beta',
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

