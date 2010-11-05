# -*- coding: utf-8 -*-
import simplejson

from openobject.tools import expose

import actions
import controllers

class Execute(controllers.SecuredController):
    _cp_path = "/openerp/execute"

    @expose()
    def index(self, action, data):
        return actions.execute(
            simplejson.loads(action),
            **simplejson.loads(data)
        )
