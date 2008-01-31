###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the 
# Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
# Boston, MA  02111-1307, USA.
#
###############################################################################

from turbogears.widgets import JSLink 

from interface import TinyField
import validators as tiny_validators

class TinyMCE(TinyField):

    template = "tinyerp.widgets.templates.tiny_mce"
    javascript = [JSLink("tinyerp", "tiny_mce/tiny_mce.js")]
    params = ["buttons"]

    def __init__(self, attrs={}):
        super(TinyMCE, self).__init__(attrs)
        self.validator = tiny_validators.String()
        
        self.buttons = """theme_advanced_toolbar_location : "top",
        theme_advanced_buttons3_add : "|,print,fullscreen"
        """

        if not self.editable:
            self.buttons = """theme_advanced_toolbar_location : "bottom",
            theme_advanced_buttons1 : "",
            theme_advanced_buttons2 : "",
            theme_advanced_buttons3 : "",
            handle_event_callback: function(){
                return false;
            }
            """

    def set_value(self, value):
        super(TinyMCE, self).set_value(value)
