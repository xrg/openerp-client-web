# -*- coding: utf-8 -*-
import openobject.tools
import openerp.utils.rpc
from openerp.controllers import SecuredController, actions

class Widgets(SecuredController):
    _cp_path = '/openerp/widgets'

    @openobject.tools.expose()
    def add(self):
        return actions.execute(
            openerp.utils.rpc.RPCProxy('res.widget.wizard').action_get({})
        )

    @openobject.tools.expose('json', methods=('POST',))
    def remove(self, widget_id):
        error = None
        try:
            openerp.utils.rpc.RPCProxy('res.widget.user').unlink(
                    widget_id, openerp.utils.rpc.session.context)
        except Exception, e:
            error = e
        return dict(error=error)

    def user_home_widgets(self, ctx):
        widgets = openerp.utils.rpc.RPCProxy('res.widget')
        user_widgets = openerp.utils.rpc.RPCProxy('res.widget.user')
        widget_ids = user_widgets.search(
                ['|',
                 ('user_id', '=', openerp.utils.rpc.session.uid),
                 ('user_id', '=', False)],
                0, 0, 0, ctx)
        return [
            dict(widgets.read([wid['widget_id'][0]], [], ctx)[0],
                 user_widget_id=wid['id'],
                 # NULL user_id = global = non-removable
                 removable=bool(wid['user_id']))
            for wid in user_widgets.read(
                    widget_ids, ['widget_id', 'user_id'], ctx)
        ]
