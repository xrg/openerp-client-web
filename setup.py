import sys

from setuptools import setup

from openobject import release

version_dash_incompatible = False
if 'bdist_rpm' in sys.argv:
    version_dash_incompatible = True
try:
    import py2exe
    version_dash_incompatible = True
except ImportError:
    pass
if version_dash_incompatible:
    release.version = release.version.split('-')[0]

setup(
    name=release.name,
    version=release.version,
    description=release.description,
    long_description=release.long_description,
    author=release.author,
    author_email=release.author_email,
    url=release.url,
    download_url=release.download_url,
    license=release.license,
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
        'openobject',
        'openobject.admin',
        'openobject.admin.i18n',
        'openobject.controllers',
        'openobject.i18n',
        'openobject.test',
        'openobject.tools',
        'openobject.widgets'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Topic :: Office/Business :: Financial',
        ],
    console=['scripts/openerp-web'],
    scripts=['scripts/openerp-web'],
    options = {'py2exe': {
        'compressed': 1,
        'optimize': 2,
        'bundle_files': 2,
        'includes': [
            'mako', 'cherrypy', 'babel', 'formencode', 'simplejson',
            'dateutil', 'pytz'
        ],
        'excludes': [
            'Carbon', 'Carbon.Files', 'Crypto', 'DNS', 'OpenSSL', 'Tkinter',
            '_scproxy', 'elementtree.ElementTree', 'email', 'email.Header',
            'email.utils', 'flup.server.fcgi', 'flup.server.scgi',
            'markupsafe._speedups', 'memcache', 'mx', 'pycountry', 'routes',
            'simplejson._speedups', 'turbogears.i18n', 'win32api', 'win32con',
            'win32event', 'win32pipe', 'win32service', 'win32serviceutil'
        ],
        'dll_excludes': [
            'w9xpopen.exe',
        ]
    }}
)
