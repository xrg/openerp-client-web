#!python

import os
import sys
import zipfile
import urllib

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

def _reporthook(numblocks, blocksize, filesize, url=None):
    base = os.path.basename(url)
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
    except:
        percent = 100
    if numblocks != 0:
        sys.stdout.write("\b"*70)
    sys.stdout.write("%-66s%3d%%" % (base, percent))

def download(url, dst=None):
    
    if not dst:
        dst = url.split('/')[-1]

    if os.path.exists(dst):
        return

    print "Downloading %s..." % (url)

    try:
        if sys.stdout.isatty():
            urllib.urlretrieve(url, dst,
                               lambda nb, bs, fs, url=url: _reporthook(nb,bs,fs,url))
            sys.stdout.write('\n')
        else:
            urllib.urlretrieve(url, dst)
    except:
        os.remove(dst)

def unzip(file, dir):
    zf = zipfile.ZipFile(file)
    for i, name in enumerate(zf.namelist()):
        if not name.endswith('/'):
            outfile = os.path.join(dir, name)
            outdir = os.path.dirname(outfile)

            if not os.path.exists(outdir):
                os.makedirs(outdir)

            outfile = open(outfile, 'wb')
            outfile.write(zf.read(name))
            outfile.flush()
            outfile.close()

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

    res = os.system("\"%s\\python.exe -c \"import pywintypes\"" % (os.path.basename(PYDIR)))
    if res == 0:
        return

    url, name = URLS['pywin32']
    download(url)

    unzip(name, 'tmp_pyw32')

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

