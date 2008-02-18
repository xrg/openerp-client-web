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

import os
import copy

from turbogears import expose
from turbogears import controllers

import cherrypy

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp.cache import cache

from tinyerp.tinyres import TinyResource
from tinyerp.utils import TinyDict

import tinyerp.widgets as tw

class View_Log(controllers.Controller, TinyResource):

    @expose(template="tinyerp.subcontrollers.templates.view_log")
    def index(self, **kw):
        params, data = TinyDict.split(kw)

        id = params.id
        model = params.model

        if not id:
            self.message_state(_('You have to select one resource!'))
            return False

        res = rpc.session.execute('object', 'execute', model, 'perm_read', [id])
        tmp = {}

        for line in res:
            todo = [
                ('id', _('ID')),
                ('create_uid', _('Creation User')),
                ('create_date', _('Creation Date')),
                ('write_uid', _('Latest Modification by')),
                ('write_date', _('Latest Modification Date')),
                ('uid', _('Owner')),
                ('gid', _('Group Owner')),
                ('level', _('Access Level'))
            ]
            for (key,val) in todo:
                if line[key] and key in ('create_uid','write_uid','uid'):
                    line[key] = line[key][1]

                tmp[key] = ustr(line[key] or '/')

        return dict(tmp=tmp, todo=todo, show_header_footer=False)

