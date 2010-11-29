import os
import glob

import babel.localedata

def babel_localedata():
    return glob.glob(
        os.path.join(babel.localedata._dirname, '*.dat')
    )

__all__ = ['opts']

opts = {
    'console': ['scripts/openerp-web'],
    'options': {'py2exe': {
        'compressed': True,
        'optimize': 2,
        'bundle_files': 2,
        'includes': [
            'mako', 'cherrypy', 'babel', 'formencode', 'simplejson', 'csv',
            'dateutil.relativedelta', 'pytz', 'xml.dom.minidom', 'cgitb',
            'mako.cache', 'zipfile'
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
            'w9xpopen.exe', "POWRPROF.dll"
        ]
    }},
    'data_files' : [
        ('babel/localedata', babel_localedata())
    ]
}
