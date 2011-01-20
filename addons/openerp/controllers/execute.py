# -*- coding: utf-8 -*-
import base64
import zlib

from openobject.tools import expose, ast

import actions
import controllers

class Execute(controllers.SecuredController):
    _cp_path = "/openerp/execute"

    @expose()
    def index(self, payload):
        decoded_payload = ast.literal_eval(
            zlib.decompress(
                base64.urlsafe_b64decode(payload)))
        action, data = decoded_payload['action'], decoded_payload['data']
        return actions.execute(action, **data)
