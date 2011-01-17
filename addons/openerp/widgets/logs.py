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

from openerp.utils import rpc

from openerp.widgets import TinyInputWidget

class Logs(TinyInputWidget):
    
    template="/openerp/widgets/templates/logs.mako"
    params=["logs"]
    
    def __init__(self, **kw):
        super(Logs, self).__init__()
        # Server log will display in flash message in form, tree view for any server action like wizard.
        self.logs = rpc.RPCProxy('res.log').get()
