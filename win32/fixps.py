import os, sys
import re

PY_DIR = os.path.dirname(sys.executable)
MY_DIR = os.path.dirname(os.path.abspath(__file__))

pat = re.compile('^#!.*$', re.M)

for f in os.listdir(MY_DIR):

    if not f.endswith('.py') or f.endswith('.pyw') or f == 'fixps.py':
        continue

    f = os.path.join(MY_DIR, f)

    src = open(f).read()
    src = pat.sub('#!"%s\python.exe"' % PY_DIR, src)

    fo = open(f, 'w')
    fo.write(src)
    fo.close()

