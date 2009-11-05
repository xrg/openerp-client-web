#!/usr/bin/env python

import sys
from os.path import join, dirname, abspath
test_path = join(dirname(abspath(__file__)), "openerp", "tests")
sys.path.insert(0, test_path)


from openerp.base.test import test

if __name__ == "__main__":
    test.run()
