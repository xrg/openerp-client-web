###############################################################################
#
#  Copyright (C) 2007-TODAY OpenERP SA. All Rights Reserved.
#
#  $Id$
#
#  Developed by OpenERP (http://openerp.com) and Axelor (http://axelor.com).
#
#  The OpenERP web client is distributed under the "OpenERP Public License".
#  It's based on Mozilla Public License Version (MPL) 1.1 with following 
#  restrictions:
#
#  -   All names, links and logos of OpenERP must be kept as in original
#      distribution without any changes in all software screens, especially
#      in start-up page and the software header, even if the application
#      source code has been changed or updated or code has been added.
#
#  You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################
import time

from openerp.utils import expr_eval, TinyDict
from openerp.widgets import TinyWidget, TinyInputWidget

from form import Form


class Record(dict):

    def __init__(self, params):

        self.params = TinyDict(**params.copy())
        self.params.view_type = 'form'

        form = Form().create_form(self.params)

        record = self._make_record(form)
        self.clear()

        self.update(record.copy())
        self['id'] = params.id or False

    def _make_record(self, parent=None):
        parent = parent or self

        for wid in parent.iter_member_widgets():

            if isinstance(wid, TinyInputWidget) and wid.name and not wid.name.endswith('/'):
                self[wid.name] = wid.get_value()

            elif isinstance(wid, TinyWidget) and len(wid.member_widgets):
                self._make_record(wid)

        params, data = TinyDict.split(self)
        return data

    def expr_eval(self, expr, source=None):
        if not isinstance(expr, basestring):
            return expr

        return expr_eval(
                expr, dict(self,
                           context=self.params.context or {},
                           active_id=self.get('id', False)))
