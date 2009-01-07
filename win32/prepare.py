#!python

import os
import sys
import zipfile
import urllib2


URLS={
    "python": ("http://www.python.org/ftp/python/2.4.4/python-2.4.4.msi", "python-2.4.4.msi"),
    "pywin32": ("http://nchc.dl.sourceforge.net/sourceforge/pywin32/pywin32-212.win32-py2.4.exe", "pywin32-212.win32-py2.4.exe"),
    "ez_setup": ("http://peak.telecommunity.com/dist/ez_setup.py", "ez_setup.py"),
    "pyxml": ("http://nchc.dl.sourceforge.net/sourceforge/pyxml/PyXML-0.8.4.win32-py2.4.exe", "PyXML-0.8.4.win32-py2.4.exe"),
    "pyparsing": ("http://pypi.python.org/packages/source/p/pyparsing/pyparsing-1.5.1.tar.gz", "pyparsing-1.5.1.tar.gz"),
}

BUILD_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
PYDIR=os.path.join(BUILD_DIR, "python24")

if not os.path.exists(BUILD_DIR):
    os.mkdir(BUILD_DIR)

os.chdir(BUILD_DIR)

def download(url, dest=None):
    if not dest:
        dest = url.split('/')[-1]

    if os.path.exists(dest):
        return

    print "Downloading", url
    try:
        src = urllib2.urlopen(url)
        data = src.read()
        fo = open(dest, "wb")
        fo.write(data)
        fo.close()
    except:
        os.remove(dest)

def check_python():

    if os.path.exists(os.path.join(PYDIR, "python.exe")):
        return True

    url, name = URLS['python']
    download(url)

    print "Extracting the the python installer..."
    os.system('msiexec /a %s /qn TARGETDIR="%s"' % (name, PYDIR))

def check_setuptools():

    res = os.system("\"%s\\python.exe -c \"import setuptools\"" % (os.path.basename(PYDIR)))
    if res == 0:
        return
    
    url, name = URLS['ez_setup']
    download(url)

    os.system("\"%s\\python.exe %s\"" % (os.path.basename(PYDIR), name))    

def check_pywin32():

    res = os.system("\"%s\\python.exe -c \"import win32api\"" % (os.path.basename(PYDIR)))
    if res == 0:
        return

    url, name = URLS['pywin32']
    download(url)

    os.system("\"%s\\python.exe -c \"from setuptools import archive_util;archive_util.unpack_archive('%s', 'tmp_pyw32')\"\"" % (os.path.basename(PYDIR), name))

    os.system("xcopy /q /y /e tmp_pyw32\\PLATLIB\\* \"%s\\Lib\\site-packages\"" % PYDIR)
    os.system("copy /y \"%s\\Lib\\site-packages\\pywin32_system32\\*\" \"%s\"" % (PYDIR, PYDIR))
    os.system("copy /y \"%s\\Lib\\site-packages\\win32\\*.exe\" \"%s\"" % (PYDIR, PYDIR))
    os.system("copy /y \"%s\\Lib\\site-packages\\win32\\*.dll\" \"%s\"" % (PYDIR, PYDIR))
    os.system("rmdir /s /q tmp_pyw32")

def check_pyxml():

    res = os.system("\"%s\\python.exe -c \"from xml import xpath\"" % (os.path.basename(PYDIR)))
    if res == 0:
        return

    url, name = URLS['pyxml']
    download(url)

    os.system("%s\\Scripts\\easy_install.exe %s" % (os.path.basename(PYDIR), name))

def check_turbogears():

    res = os.system("\"%s\\python.exe -c \"import turbogears\"" % (os.path.basename(PYDIR)))
    if res == 0:
        return

    os.system("%s\\Scripts\\easy_install.exe -x -Z TurboGears==1.0.8" % os.path.basename(PYDIR))

def check_pyparsing():

    res = os.system("\"%s\\python.exe -c \"import pyparsing\"" % (os.path.basename(PYDIR)))
    if res == 0:
        return

    url, name = URLS['pyparsing']
    download(url)

    os.system("%s\\Scripts\\easy_install.exe -x -Z %s" % (os.path.basename(PYDIR), name))

def check_openerp_web():

    res = os.system("\"%s\\python.exe -c \"from openerp import widgets\"" % (os.path.basename(PYDIR)))
    if res == 0:
        return

    os.system("%s\\Scripts\\easy_install.exe -Z -N ..\\.." % os.path.basename(PYDIR))

def check_fixps():
    os.system("copy /y ..\\fixps.py \"%s\\Scripts\"" % PYDIR)

def prepare():
    check_python()
    check_setuptools()
    check_pywin32()
    check_pyxml()
    check_turbogears()
    check_pyparsing()
    check_openerp_web()
    check_fixps()

if __name__ == "__main__":
    prepare()

