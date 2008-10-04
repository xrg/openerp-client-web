###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

class TinyException(Exception):

    def __init__(self, message, title=None):

        self.title = title
        self.message = message

    def __unicode__(self):
        return ustr(self.message)
    
    def __str__(self):
        return self.message

class TinyError(TinyException):

    def __init__(self, message, title=_("Error")):
        TinyException.__init__(self, message=message, title=title)

class TinyWarning(TinyException):

    def __init__(self, message, title=_("Warning")):
        TinyException.__init__(self, message=message, title=title)

class TinyMessage(TinyException):

    def __init__(self, message, title=_("Information")):
        TinyException.__init__(self, message=message, title=title)

def error(title, msg, details=None):
    raise TinyError(message=msg, title=title or _("Error"))

def warning(msg, title=None):
    raise TinyWarning(message=msg, title=title or _("Warning"))

def message(msg):
    raise TinyMessage(message=msg)

def to_xml(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

# vim: ts=4 sts=4 sw=4 si et

