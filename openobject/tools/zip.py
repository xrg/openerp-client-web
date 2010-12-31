# -*- coding: utf-8 -*-
import os
import shutil
import zipfile

def extract_zip_file(zip_file, outdirectory):
    zf = zipfile.ZipFile(zip_file)
    out = outdirectory
    for path in zf.namelist():
        tgt = os.path.join(out, path)
        tgtdir = os.path.dirname(tgt)
        if not os.path.exists(tgtdir):
            os.makedirs(tgtdir)

        if not tgt.endswith(os.sep):
            fp = open(tgt, 'wb')
        fp.write(zf.read(path))
        fp.close()
    zf.close()


