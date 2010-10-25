#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Start script for the openerp-web project.

This script is only needed during development for running from the project
directory. When the project is installed, easy_install will create a
proper start script.
"""

import sys
from openobject.commands import start, ConfigurationError

if __name__ == "__main__":
    try:
        start()
    except ConfigurationError, exc:
        sys.stderr.write(str(exc)+"\n")
        sys.exit(1)

# vim: ts=4 sts=4 sw=4 si et

