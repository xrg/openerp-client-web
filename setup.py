#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import re
import sys

from setuptools import setup, find_packages


execfile(os.path.join("openobject", "release.py"))

version_dash_incompatible = False
if (len(sys.argv) > 1) and 'bdist_rpm' in sys.argv:
    version_dash_incompatible = True
try:
    import py2exe
    from py2exe_utils import opts
    version_dash_incompatible = True
except ImportError:
    opts = {}
if version_dash_incompatible:
    version = version.split('-')[0]

FILE_PATTERNS = \
    r'.+\.(py|cfg|po|pot|mo|txt|rst|gif|png|jpg|ico|mako|html|js|css|htc|swf)$'    
def find_data_files(source, dest=None, patterns=FILE_PATTERNS):
    file_matcher = re.compile(patterns, re.I)
    if dest is None: dest = source
    out = []
    for base, _, files in os.walk(source):
        source_dir = os.path.relpath(base, source)
        dest_dir = os.path.join(dest, source_dir)
        cur_files = []
        for f in files:
            if file_matcher.match(f):
                cur_files.append(os.path.join(
                    source, source_dir, f))
        if cur_files:
            out.append(
                (dest_dir, cur_files))

    return out

def find_all_packages(modlist):
    """A helper to find all python modules under some name.
    
    Example, given modlist=['addons.openerp'] it will scan and
    find ['addons.openerp', 'addons.openerp.controllers', ...]
    """
    res = []
    for mod in modlist:
	res.append(mod)
	for submod in find_packages(mod.replace('.','/')):
	    res.append(mod + '.' + submod)
    return res

DATAFILE_GLOBS = [ 
        '*.cfg',
        '*.po', '*.pot',
        '*.mo', # ?
        '*.txt', '*.rst',
        '*.gif', '*.png', '*.jpg', '*.ico',
        '*.mako', '*.html', '*.js', '*.css',
        '*.htc', '*.swf' ]

DATAFILE_GLOBS_O = [
        '*.cfg', '*.css', '*.js', '*.mako',
        '*.gif', '*.png', '*.jpg', '*.ico'
        ]

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=url,
    download_url=download_url,
    license=license,
    include_package_data=True,
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
        'openobject.widgets',
    ] + find_all_packages( [
        'addons.openerp',
        'addons.view_calendar',
        'addons.view_diagram',
        'addons.view_graph',
        'addons.widget_ckeditor',
        ] ),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Topic :: Office/Business :: Financial',
        ],
    scripts=['scripts/openerp-web'],
    data_files=(find_data_files('doc', dest=os.path.join('doc', 'openerp-web'), patterns='')
              + opts.pop('data_files', [])
    ),
    **opts
)
