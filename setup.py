import os
import re
import sys

from setuptools import setup

from openobject import release

version_dash_incompatible = False
if 'bdist_rpm' in sys.argv:
    version_dash_incompatible = True
try:
    import py2exe
    from py2exe_utils import opts
    version_dash_incompatible = True
except ImportError:
    opts = {}
if version_dash_incompatible:
    release.version = release.version.split('-')[0]

FILE_PATTERNS = re.compile(
    r'.+\.(py|cfg|po|pot|mo|txt|rst|gif|png|jpg|ico|mako|html|js|css|htc|swf)$', re.I)
def find_data_files(source, dest=None):
    if dest is None: dest = source
    out = []
    for base, _, files in os.walk(source):
        source_dir = os.path.relpath(base, source)
        dest_dir = os.path.join(dest, source_dir)
        cur_files = []
        for f in files:
            if FILE_PATTERNS.match(f):
                cur_files.append(os.path.join(
                    source, source_dir, f))
        if cur_files:
            out.append(
                (dest_dir, cur_files))

    return out

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
    scripts=['scripts/openerp-web'],
    data_files=(find_data_files('addons/openerp')
              + find_data_files('addons/view_calendar')
              + find_data_files('addons/view_diagram')
              + find_data_files('addons/view_graph')
              + find_data_files('addons/widget_ckeditor')
               ),
    package_data={
        'openobject.admin.i18n': ['mapping/*.cfg'],
        'openobject.controllers': ['base.mako'],
        'openobject': [
            'static/css/jquery-ui/smoothness/images/*.png',
            'static/css/jquery-ui/smoothness/images/*.gif',
            'static/css/jquery-ui/smoothness/jquery-ui-1.8.2.custom.css',
            'static/css/jquery.fancybox-1.3.1.css',
            'static/images/*.gif',
            'static/images/*.ico',
            'static/images/fancybox/*.png',
            'static/javascript/jQuery/*.js',
            'static/javascript/MochiKit/*.js',
            'static/javascript/openobject/*.js'
        ]
    },
    **opts
)
