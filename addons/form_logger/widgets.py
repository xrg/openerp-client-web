# -*- coding: utf-8 -*-
import openobject.meta

import openerp.widgets.sidebar

class Sidebar(openerp.widgets.sidebar.Sidebar, openobject.meta.Extends):
    params = ['piratepad']
    def __init__(self, *args, **kwargs):
        super(Sidebar, self).__init__(*args, **kwargs)
        self.piratepad = {
            'name': 'OpenERP web bugs',
            'pad': 'openerp-web-bugs'
        }
