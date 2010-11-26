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
        """ user_home_widgets(context) -> [{'title':unicode, 'content':unicode, 'removable':bool, 'user_widget_id':object}]

        Returns a list of the widgets to display on the user's home page.

        The widgets list contains both user-widgets (`removable` key set to
        True) and global widgets (`removable` key set to False), the latter
        being created and managed by the local adminstrator rather than the
        current user.

        The `user_widget_id` key is the id of the corresponding
        `res.widget.user`, which will be deleted if the user removes
        a widget from his home page (or created if he adds one)
        """
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
