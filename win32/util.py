import os
import sys
import zipfile
import urllib

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
