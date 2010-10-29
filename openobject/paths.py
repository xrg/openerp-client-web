# -*- coding: utf-8 -*-
import os
import pkg_resources
import sys

__all__ = ['addons']

# TODO: get from config file?
ROOT_PATH = None
try:
    ROOT_PATH = pkg_resources.resource_filename('openobject', '..')
except NotImplementedError:
    # pkg_resource hate
    pass
if not (ROOT_PATH and os.path.exists(ROOT_PATH)):
    if not hasattr(sys, 'frozen'):
        # regular install, addons is part of the openerp-web distribution
        ROOT_PATH = pkg_resources.resource_filename(
                pkg_resources.Requirement.parse('openerp-web'), '')
    else:
        # py2exe package
        # in a py2exe system, sys.executable is the name of the py2exe executable/bundle
        # and that executable is at our root
        ROOT_PATH = os.path.dirname(sys.executable)
ROOT_PATH = os.path.normpath(ROOT_PATH)

ADDONS_PATH = os.path.join(ROOT_PATH, 'addons')
assert os.path.isdir(ADDONS_PATH), "Unable to locate addons."

sys.path.insert(0, ADDONS_PATH)

def addons(*sections): return os.path.join(ADDONS_PATH, *sections)
def root(*sections): return os.path.join(ROOT_PATH, *sections)
