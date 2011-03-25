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

from openobject.widgets import JSLink

from openerp import validators

from openerp.widgets import TinyInputWidget
from openerp.widgets import register_widget



__all__ = ["CKEditor"]

class CKEditor(TinyInputWidget):

    template = "/widget_ckeditor/widgets/templates/ckeditor.mako"

    javascript = [JSLink("widget_ckeditor", "javascript/ck_editor/ckeditor.js"),
                  JSLink("widget_ckeditor", "javascript/ck_editor/adapters/jquery.js")]

    def __init__(self, **attrs):
        super(CKEditor, self).__init__(**attrs)
        self.validator = validators.String()
        self.readonly = not self.editable or self.readonly

    def set_value(self, value):
        super(CKEditor, self).set_value(value)

register_widget(CKEditor, ["text_html"])

# vim: ts=4 sts=4 sw=4 si et

