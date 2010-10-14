import os
import sys

from distutils.core import setup
from distutils.core import Command
from distutils.errors import *

import fnmatch
import util

URLS = {
    "python": ("http://www.python.org/ftp/python/2.5.4/python-2.5.4.msi", "python-2.5.4.msi"),
    "ez_setup": ("http://peak.telecommunity.com/dist/ez_setup.py", "ez_setup.py"),
    "pywin32": ("http://nchc.dl.sourceforge.net/sourceforge/pywin32/pywin32-212.win32-py2.5.exe", "pywin32-212.win32-py2.5.exe")
}

BUILD_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
PYDIR=os.path.join(BUILD_DIR, "python25")

execfile(os.path.join("openobject", "release.py"))

class bdist_wininst(Command):
    user_options = [('allinone', None, 'Generate the windows installer for the All In One')]

    def initialize_options (self):
        self.allinone = None

    def finalize_options (self):
        pass

    def run (self):

        if (sys.platform != "win32"):
            raise DistutilsPlatformError("Distribution must be compiled on a Windows 32 platform")

        if not os.path.exists(BUILD_DIR):
            os.mkdir(BUILD_DIR)

        # change to the build dir
        os.chdir(BUILD_DIR)

        self._check_python()
        self._check_setuptools()
        self._check_pywin32()
        self._check_openerp_web()
        self._check_fixps()

        for package in [
            ('cherrypy', 'CherryPy >= 3.1.2'),
            ('mako', 'mako >= 0.2.4'),
            ('babel', 'Babel >= 0.9.4'),
            ('formencode', 'FormEncode >= 1.2.2'),
            ('simplejson', 'simplejson >= 2.0.9'),
            ('dateutil', 'python-dateutil >= 1.4.1'),
            ('pytz', 'pytz >= 2009j')
            ]:
            self._check_package(*package)

        # finally compile the setup.nsi
        self._make_nsis()

    def run_py(self, *args):
        return not os.system(PYDIR + "\\python.exe " + " ".join(args))

    def run_ez(self, *args):
        return not os.system(PYDIR + "\\Scripts\\easy_install.exe -Z " + " ".join(args))

    def check_module(self, module):
        return self.run_py('-c', '"import %s"' % module)

    def _check_python(self):

        if os.path.exists(os.path.join(PYDIR, "python.exe")):
            return True

        url, name = URLS['python']
        util.download(url)

        print "Extracting the the python installer..."
        os.system('msiexec /a %s /qn TARGETDIR="%s"' % (name, PYDIR))

    def _check_setuptools(self):

        if self.check_module("setuptools"):
            return

        url, name = URLS['ez_setup']
        util.download(url)

        self.run_py(name)

    def _check_pywin32(self):

        if self.check_module("pywintypes"):
            return

        url, name = URLS['pywin32']
        util.download(url, name)

        util.unzip(name, 'tmp_pyw32')

        os.system("xcopy /q /y /e tmp_pyw32\\PLATLIB\\* \"%s\\Lib\\site-packages\"" % PYDIR)
        os.system("copy /y \"%s\\Lib\\site-packages\\pywin32_system32\\*\" \"%s\"" % (PYDIR, PYDIR))
        os.system("copy /y \"%s\\Lib\\site-packages\\win32\\*.exe\" \"%s\"" % (PYDIR, PYDIR))
        os.system("copy /y \"%s\\Lib\\site-packages\\win32\\*.dll\" \"%s\"" % (PYDIR, PYDIR))
        os.system("rmdir /s /q tmp_pyw32")

    def _check_package(self, package, dependency):
        if self.check_module(package):
            return
        self.run_ez(dependency)

    def _check_pyparsing(self):

        if self.check_module("pyparsing"):
            return

        url, name = URLS['pyparsing']
        util.download(url, name)

        self.run_ez(name)

    def _check_openerp_web(self):

        if self.check_module("openobject"):
            # remove old version
            self.run_ez("-m", "openerp-web")

            for f in os.listdir("%s\\Scripts" % PYDIR):
                if fnmatch.fnmatch(f, "*openerp-web*"):
                    os.remove(os.path.join(PYDIR, "Scripts", f))

            for f in os.listdir("%s\\Lib\\site-packages" % PYDIR):
                if fnmatch.fnmatch(f, "openerp_web*"):
                    os.system("rd /s /q \"%s\\Lib\\site-packages\\%s\"" %(PYDIR, f))

        self.run_ez("-N", "..\\..")

    def _check_fixps(self):
        os.system("copy /y ..\\fixps.py \"%s\\Scripts\"" % PYDIR)

    def _make_nsis(self):

        #TODO: read registry
        makensis = "C:\\Program Files\\NSIS\\makensis.exe"
        if not os.path.exists(makensis):
            makensis = "makensis.exe"

        cmd = '"%s" %s /DVERSION=%s ..\\setup.nsi' % (makensis,
                                                      self.allinone and '/DALLINONE=1' or '',
                                                      version,)

        os.system(cmd)

setup(cmdclass={'bdist_wininst': bdist_wininst})

