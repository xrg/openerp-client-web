###############################################################################
#
# Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
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
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
###############################################################################

"""
This module implements TurboGear controllers to perform most standard actions
on Tiny models like `create`, `write`, `unlink` etc.
"""

from turbogears import controllers
from turbogears import expose

from tinyerp import rpc
from tinyerp.tinyres import TinyResource

import gui

def make_dict(data):
    """Generate dictionary for TinyERP object from the given data.

    @param data: the data retrived from the web form

    @rtype: dict
    @return: a dictionary
    """

    res = {}
    for name, value in data.items():
        names = name.split('/')

        if len(names) > 1:
            res.setdefault(names[0], {}).update({"/".join(names[1:]): value})
        else:
            res[name] = value or False

    for k, v in res.items():
        if type(v) == type({}):
            #res[k] = make_dict(v)

            id = 0
            if '__id' in v:
                id = int(v.pop('__id'))

            res[k] = [(id and 1, id, make_dict(v))]

    return res

def make_view_id(view_id):
    if view_id == 'True':
        return True
    if view_id == 'False':
        return False

    if view_id:
        return int(view_id)
    else:
        return False

class TinyMethod(controllers.Controller, TinyResource):
    """Base class for all methods
    """
    pass

class Edit(TinyMethod):

    @expose()
    def default(self, view_id, model, id=None):
        view_id = make_view_id(view_id)
        return gui.form.create(view_id, model, id)

class Save(TinyMethod):

    @expose()
    def default(self, view_id, model, id=None, **data):

        data_dict = make_dict(data)
        view_id = make_view_id(view_id)

        message=None
        try:
            if not id:
                proxy = rpc.RPCProxy(model)
                res = proxy.create(data_dict) #TODO: context?
                id = int(res)
                message = "Saved successfully..."
            else:
                id = int(id)
                proxy = rpc.RPCProxy(model)
                res = proxy.write([id], data_dict) #TODO: context?
                message = "Updated successfully..."
        except Exception, e:
            message=str(e)

        return gui.form.create(view_id=view_id, model=model, id=id, message=message)

class Delete(TinyMethod):

    @expose()
    def default(self, view_id, model, id):
        try:
            id = int(id)
            proxy = rpc.RPCProxy(model)
            res = proxy.unlink([id])
            message = "Record deleted sucessfully..."
        except Exception, e:
            message=str(e)

        view_id = make_view_id(view_id)

        return gui.form.create(view_id=view_id, model=model, message=message)

class Find(TinyMethod):
    """Cotroller method to search records.
    """

    @expose()
    def default(self, model):
        """Show search window to find records of the given model.

        @param model: the model

        @return: view of the search window
        """
        return gui.search.create(model)
