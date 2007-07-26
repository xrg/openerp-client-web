from setuptools import setup, find_packages
from turbogears.finddata import find_package_data

import os
execfile(os.path.join("tinyerp", "release.py"))

packages=find_packages()
package_data = find_package_data(where='tinyerp',
    package='tinyerp')
if os.path.isdir('locales'):
    packages.append('locales')
    package_data.update(find_package_data(where='locales',
        exclude=('*.po',), only_in_packages=False))

setup(
    name="eTiny",
    version=version,

    # uncomment the following lines if you fill them out in release.py
    description='Tiny ERP is a free enterprise management software: accounting, stock, manufacturing, project mgt, ... eTiny is the web client of the Tiny ERP project',
    author='Tiny ERP Pvt. Ltd.',
    author_email='info@tinyerp.com',
    url='http://www.tinyerp.com/demonstration.html',
    download_url='http://tinyerp.com',
    license='GPL',

    install_requires=[
        "TurboGears >= 1.0.3.2",
    ],
    scripts=["start-tinyerp.py"],
    zip_safe=False,
    packages=packages,
    package_data=package_data,
    keywords=[
        # Use keywords if you'll be adding your package to the
        # Python Cheeseshop

        # if this has widgets, uncomment the next line
        # 'turbogears.widgets',

        # if this has a tg-admin command, uncomment the next line
        # 'turbogears.command',

        # if this has identity providers, uncomment the next line
        # 'turbogears.identity.provider',

        # If this is a template plugin, uncomment the next line
        # 'python.templating.engines',

        # If this is a full application, uncomment the next line
        'turbogears.app',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: TurboGears',
        # if this is an application that you'll distribute through
        # the Cheeseshop, uncomment the next line
        'Framework :: TurboGears :: Applications',

        # if this is a package that includes widgets that you'll distribute
        # through the Cheeseshop, uncomment the next line
        # 'Framework :: TurboGears :: Widgets',
    ],
    test_suite='nose.collector',
    )
