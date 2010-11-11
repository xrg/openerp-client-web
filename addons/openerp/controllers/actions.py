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
# -   All distributions of     the software must keep source code with OEPL.
#
# -   All integrations to any other software must keep source code with OEPL.
#
# If you need commercial licence to remove this kind of restriction please
# contact us.
#
# You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################

"""This module implementes action methods.
"""
import base64
import time

import cherrypy
from openerp.utils import rpc, common, expr_eval, TinyDict

from form import Form
from openobject import tools
from selection import Selection
from tree import Tree
from wizard import Wizard
import urllib
import simplejson

def execute_window(view_ids, model, res_id=False, domain=None, view_type='form', context=None,
                   mode='form,tree', name=None, target=None, limit=None, search_view=None,
                   context_menu=False, display_menu_tip=False):
    """Performs `actions.act_window` action.

    @param view_ids: view ids
    @param model: a model for which the action should be performed
    @param res_id: resource id
    @param domain: domain
    @param view_type: view type, eigther `form` or `tree`
    @param context: the context
    @param mode: view mode, eigther `form,tree` or `tree,form` or None

    @return: view (mostly XHTML code)
    """

    params = TinyDict()

    params.model = model
    params.ids = res_id
    params.view_ids = view_ids
    params.domain = domain or []
    params.context = context or {}
    params.limit = limit
    params.search_view = search_view
    params['context_menu'] = context_menu
    params['display_menu_tip'] = display_menu_tip

    cherrypy.request._terp_view_name = name or None
    cherrypy.request._terp_view_target = target or None
    if name:
        params.context['_terp_view_name'] = name

    if params.ids and not isinstance(params.ids, list):
        params.ids = [params.ids]

    params.id = (params.ids or False) and params.ids[0]

    mode = mode or view_type
    if view_type == 'form':
        mode = mode.split(',')
        params.view_mode=mode

        return Form().create(params)

    elif view_type == 'tree':
        return Tree().create(params)

    else:
        raise common.message(_("Invalid View"))

def execute_wizard(name, **datas):
    """Executes given wizard with the given data

    @param name: name of the wizard
    @param datas: datas

    @return: wizard view (mostly XHTML code)
    """
    params = TinyDict()
    params.name = name
    params.datas = datas
    params.state = 'init'

    return Wizard().create(params)

PRINT_FORMATS = {
     'pdf' : 'application/pdf',
     'doc' : 'application/vnd.ms-word',
     'html': 'text/html',
     'sxw' : 'application/vnd.sun.xml.writer',
     'odt' : 'application/vnd.oasis.opendocument.text',
     'ods' : 'application/vnd.oasis.opendocument.spreadsheet',
     'xls' : 'application/vnd.ms-excel',
     'doc' : 'application/msword',
     'csv' : 'text/csv',
     'rtf' : 'application/rtf',
     'txt' : 'text/plain',
}

def _print_data(data):

    if 'result' not in data:
        raise common.message(_('Error no report'))

    if data.get('code','normal')=='zlib':
        import zlib
        content = zlib.decompress(base64.decodestring(data['result']))
    else:
        content = base64.decodestring(data['result'])

    cherrypy.response.headers['Content-Type'] = PRINT_FORMATS[data['format']]
    return content

def execute_report(name, **data):
    """Executes a report with the given data, on success returns `application/pdf` data

    @param name: name of the report
    @param data: report data

    @return: `application/pdf` data
    """
    datas = data.copy()
    ids = datas['ids']
    del datas['ids']

    if not ids:
        ids =  rpc.session.execute('object', 'execute', datas['model'], 'search', [])
        if ids == []:
            raise common.message(_('Nothing to print'))

        datas['id'] = ids[0]

    try:
        ctx = dict(rpc.session.context)
        ctx.update(datas.get('context', {}))
        report_id = rpc.session.execute('report', 'report', name, ids, datas, ctx)
        state = False
        attempt = 0
        val = None
        while not state:
            val = rpc.session.execute('report', 'report_get', report_id)
            if not val:
                return False
            state = val['state']
            if not state:
                time.sleep(1)
                attempt += 1
            if attempt>200:
                raise common.message(_('Printing aborted, too long delay'))

        # report name
        report_name = 'report'
        report_type = val['format']

        if name != 'custom':
            proxy = rpc.RPCProxy('ir.actions.report.xml')
            res = proxy.search([('report_name','=', name)])
            if res:
                report_name = proxy.read(res[0], ['name'])['name']

        report_name = report_name.replace('Print ', '')
        cherrypy.response.headers['Content-Disposition'] = 'filename="' + report_name + '.' + report_type + '"'

        return _print_data(val)

    except rpc.RPCException, e:
        raise e

def act_window_close(*args):
    return close_popup()

def act_window(action, data):
    for key in ('res_id', 'res_model', 'view_type',
                'view_mode', 'limit', 'search_view'):
        data[key] = action.get(key, data.get(key))
    if not data.get('search_view') and data.get('search_view_id'):
        data['search_view'] = str(rpc.session.execute(
                'object', 'execute', data['res_model'], 'fields_view_get',
                data['search_view_id'], 'search', data['context']))
    if not data.get('limit'):
        data['limit'] = 50
    view_ids = False
    if action.get('views', []):
        if isinstance(action['views'], list):
            view_ids = [x[0] for x in action['views']]
            data['view_mode'] = ",".join([x[1] for x in action['views']])
        else:
            if action.get('view_id'):
                view_ids = [action['view_id'][0]]
    elif action.get('view_id'):
        view_ids = [action['view_id'][0]]
    if not action.get('domain'):
        action['domain'] = '[]'

    ctx = dict(data.get('context', {}),
        active_id=data.get('id', False),
        active_ids=data.get('ids', []),
        active_model=data.get('model', False)
    )
    ctx.update(expr_eval(action.get('context', '{}'), ctx))

    search_view = action.get('search_view_id')
    if search_view:
        if isinstance(search_view, (list, tuple)):
            ctx['search_view'] = search_view[0]
        else:
            ctx['search_view'] = search_view

        # save active_id in session
    rpc.session.active_id = data.get('id')
    domain = expr_eval(action['domain'], ctx)
    if data.get('domain'):
        domain.append(data['domain'])

    if 'menu' in data['res_model'] and action.get('name') == 'Menu':
        return close_popup()

    if action.get('display_menu_tip'):
        display_menu_tip = action.get('help')
    else:
        display_menu_tip = None

    return execute_window(view_ids,
                          data['res_model'],
                          data['res_id'],
                          domain,
                          action['view_type'],
                          ctx, data['view_mode'],
                          name=action.get('name'),
                          target=action.get('target'),
                          limit=data.get('limit'),
                          search_view=data['search_view'],
                          context_menu=data.get('context_menu'),
                          display_menu_tip=display_menu_tip)

def server(action, data):
    context = dict(data.get('context', {}),
        active_id=data.get('id', False),
        active_ids=data.get('ids', [])
    )
    action_result = rpc.RPCProxy('ir.actions.server').run([action['id']], context)
    if action_result:
        if not isinstance(action_result, list):
            action_result = [action_result]

        output = ''
        for r in action_result:
            output = execute(r, **data)
        return output
    else:
        return ''

def wizard(action, data):
    if 'window' in data:
        del data['window']
    data['context'] = dict(
        data.get('context', {}),
        **action.get('context', {})
    )
    return execute_wizard(action['wiz_name'], **data)

def custom_report(action, data):
    data.update(action.get('datas', {}))
    data['report_id'] = action['report_id']
    return report_link('custom', **data)

def xml_report(action, data):
    data.update(action.get('datas', {}))
    return report_link(action['report_name'], **data)

def act_url(action, data):
    return execute_url(**dict(data,
        url=action['url'],
        target=action['target'],
        type=action['type']
    ))

ACTIONS_BY_TYPE = {
    'ir.actions.act_window_close': act_window_close,
    'ir.actions.act_window': act_window,
    'ir.actions.submenu': act_window,
    'ir.actions.server': server,
    'ir.actions.wizard': wizard,
    'ir.actions.report.custom': custom_report,
    'ir.actions.report.xml': xml_report,
    'ir.actions.act_url': act_url
}

NEW_WINDOW_NAME = 'openerp_popup'
def execute_opener(action, data):
    # Add 'opened' mark to indicate we're now within the popup and can
    # continue on during the second round of execution
    url = ('/openerp/execute?' + urllib.urlencode({
        'action': simplejson.dumps(dict(action, opened=True)),
        'data': simplejson.dumps(data)
    }))
    cherrypy.response.headers['X-Target'] = 'new'
    cherrypy.response.headers['Location'] = url
    cherrypy.response.headers['X-New-Window-Name'] = NEW_WINDOW_NAME
    return """<script type="text/javascript">
        window.open('%s', '%s', "width=800,height=600");
    </script>
    """ % (url, NEW_WINDOW_NAME)

def execute(action, **data):
    """Execute the action with the provided data. for internal use only.

    @param action: the action
    @param data: the data

    @return: mostly XHTML code
    """
    if 'type' not in action:
        #XXX: in gtk client just returns to the caller
        #raise common.error('Error', 'Invalid action...')
        return close_popup()

    if action.get('target') == 'new' and not action.get('opened'):
        return execute_opener(action, data)

    data.setdefault('context', {}).update(expr_eval(action.get('context','{}'), data.get('context', {}).copy()))

    action_executor = ACTIONS_BY_TYPE[action['type']]
    return action_executor(action, data)

def execute_url(**data):
    url = data.get('url') or ''

    if not ('://' in url or url.startswith('/')):
        raise common.message(_('Relative URLs are not supported'))
    
    # Unknown URL required to open in new window/tab.
    if url.startswith('http://') or url.startswith('http://'):
        return """<html>
                <head>
                    <script language="javascript" type="text/javascript">
                        window.open('%s')
                    </script>
                </head>
                <body></body>
                </html>
                """ % (tools.redirect(url)[0][0])
    else:
        return """<html>
                    <head>
                        <script language="javascript" type="text/javascript">
                            openLink('%s')
                        </script>
                    </head>
                </html>
                """ % (tools.redirect(url)[0][0])
    

def get_action_type(act_id):
    """Get the action type for the given action id.

    @param act_id: the action id
    @return: action type
    """

    proxy = rpc.RPCProxy("ir.actions.actions")
    res = proxy.read([act_id], ["type"], rpc.session.context)[0]

    if not (res and len(res)):
        raise common.message(_('Action not found'))

    return res['type']

def execute_by_id(act_id, type=None, **data):
    """Perforns the given action of type `type` with the provided data.

    @param act_id: the action id
    @param type: action type
    @param data: the data

    @return: JSON object or XHTML code
    """

    if type is None:
        type = get_action_type(act_id)
        
    ctx = dict(rpc.session.context, **(data.get('context') or {}))   

    res = rpc.session.execute('object', 'execute', type, 'read', act_id, False, ctx)
    return execute(res, **data)

def execute_by_keyword(keyword, adds=None, **data):
    """Performs action represented by the given keyword argument with given data.

    @param keyword: action keyword
    @param data: action data

    @return: XHTML code
    """

    actions = None
    if 'id' in data:
        try:
            id = data.get('id', False)
            if (id): id = int(id)
            actions = rpc.session.execute('object', 'execute', 'ir.values', 'get', 'action', keyword, [(data['model'], id)], False, rpc.session.context)
            actions = map(lambda x: x[2], actions)
        except rpc.RPCException, e:
            raise e

    keyact = {}
    action = None
    for action in actions:
        keyact[action['name']] = action

    keyact.update(adds or {})

    if not keyact:
        raise common.message(_('No action defined'))

    if len(keyact) == 1:
        if data.get('context'):
            data['context'].update(rpc.session.context)
        else:
            data['context'] = rpc.session.context
        return execute(action, **data)
    else:
        return Selection().create(keyact, **data)


@tools.expose(template="/openerp/controllers/templates/closepopup.mako")
def close_popup(*args, **kw):
    return dict()

@tools.expose(template="/openerp/controllers/templates/report.mako")
def report_link(report_name, **kw):
    return dict(name=report_name, data=kw)
    
