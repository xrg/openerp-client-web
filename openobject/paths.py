# -*- coding: utf-8 -*-
import os
import pkg_resources
import sys

__all__ = ['addons']

# TODO: get from config file?
ADDONS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "addons")
if not os.path.exists(ADDONS_PATH):
    if not hasattr(sys, 'frozen'):
        # regular install
        ADDONS_PATH = pkg_resources.resource_filename(
                pkg_resources.Requirement.parse('openerp-web'), 'addons')
    else:
        # py2exe package
        ADDONS_PATH = os.path.join(
            # in a py2exe system, sys.executable is the name of the py2exe executable/bundle
            os.path.dirname(sys.executable),
            'addons'
        )

assert os.path.isdir(ADDONS_PATH), "Unable to locate addons."

sys.path.insert(0, ADDONS_PATH)

def addons(): return ADDONS_PATH
