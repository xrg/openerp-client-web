import os
import sys

from setuptools import setup


execfile(os.path.join("openobject", "release.py"))

if 'bdist_rpm' in sys.argv:
    version = version.split('-')[0]


setup(
    name="openerp-web",
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=email,
    url=url,
    download_url=download_url,
    copyright=copyright,
    license=license,
    install_requires=[
        "CherryPy >= 3.1.2",
        "Mako >= 0.2.4",
        "Babel >= 0.9.4",
        "FormEncode >= 1.2.2",
        "simplejson >= 2.0.9",
        "python-dateutil >= 1.4.1",
        "pytz >= 2009j"
    ],
    zip_safe=False,
    packages=[
        'openerp-web.openobject', 
        'openerp-web.addons',
        'openerp-web.scripts',
        'openerp-web.doc',],
    package_dir={
        'openerp-web.scripts': 'scripts',
        'openerp-web.openobject': 'openobject',
        'openerp-web.addons': 'addons',
        'openerp-web.doc': 'doc',
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Topic :: Office/Business :: Financial',
        ],
    scripts=['scripts/openerp-web'],
)

# vim: ts=4 sts=4 sw=4 si et

