###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# The OpenERP web client is distributed under the "OpenERP Public License".
# It's based on Mozilla Public License Version (MPL) 1.1 with following
# restrictions:
#
# -   All names, links and logos of Tiny, OpenERP and Axelor must be
#     kept as in original distribution without any changes in all software
#     screens, especially in start-up page and the software header, even if
#     the application source code has been changed or updated or code has been
#     added.
#
# -   All distributions of the software must keep source code with OEPL.
#
# -   All integrations to any other software must keep source code with OEPL.
#
# If you need commercial licence to remove this kind of restriction please
# contact us.
#
# You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
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

class Concurrency(Exception):

    def __init__(self, message, title=None, datas=None):
        self.title = title
        self.datas = datas
        self.message = message

    def __unicode__(self):
        return ustr(self.title)

    def __str__(self):
        return self.title

def error(title, msg):
    raise TinyError(message=msg, title=title or _("Error"))

def warning(msg, title=None):
    raise TinyWarning(message=msg, title=title or _("Warning"))

def message(msg):
    raise TinyMessage(message=msg)

def to_xml(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def concurrency(msg, title=None, datas=None):
    raise Concurrency(message=msg, title=title, datas=datas)

# vim: ts=4 sts=4 sw=4 si et
