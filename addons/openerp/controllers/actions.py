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

"""This module implementes action methods.
"""
import base64
import time
import urlparse
import zlib

import cherrypy
from openerp.utils import rpc, common, expr_eval, TinyDict

from form import Form
from openobject import tools
from selection import Selection
from tree import Tree
from wizard import Wizard
import urllib

def execute_window(view_ids, model, res_id=False, domain=None, view_type='form', context=None,
                   mode='form,tree', name=None, target=None, limit=None, search_view=None,
                   context_menu=False, display_menu_tip=False, action_id=None):
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
    params['target'] = target or None
    cherrypy.request._terp_view_name = name or None
    cherrypy.request._terp_view_target = target or None

    if action_id:
        params.action_id = action_id

    if name:
         params.context['_terp_view_name'] = name
    else:
        if params.context.get('_terp_view_name'):
            del params.context['_terp_view_name']
    
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
        if not ids:
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
    if not action.get('opened'):
        action.setdefault('target', 'current')
        return act_window_opener(action, data)

    for key in ('res_id', 'res_model', 'view_type',
                'view_mode', 'limit', 'search_view'):
        data[key] = action.get(key, data.get(key))
    if not data.get('search_view') and data.get('search_view_id'):
        data['search_view'] = str(rpc.session.execute(
                'object', 'execute', data['res_model'], 'fields_view_get',
                data['search_view_id'], 'search', data['context']))
    if data.get('limit'):
        data['limit'] = 20
    
    if action.get('target') and action['target'] == 'popup' and action.get('res_model') and isinstance(action.get('context'), dict):
        search_view_id = rpc.RPCProxy('ir.ui.view').search([('type','=', 'search'), ('model','=',action['res_model'])], 0, 0, 0, rpc.session.context)
        if search_view_id and action['context'].get('search_view'):
            action['context']['search_view'] = search_view_id[0]
    
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
    
    if action.get('context') and isinstance(action['context'], dict):
        if not action['context'].get('active_ids'):
            action['context']['active_ids'] = ctx['active_ids'] or []
    
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
                          display_menu_tip=display_menu_tip,
                          action_id=action.get('id'))

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

def act_window_opener(action, data):
    # Action of target 'current' (or no target) should open in a new tab
    # unless it is triggered from a menu
    # or if it is not tied to an object (ex: home action after login)
    open_new_tab = False
    if action['target'] == 'current' and action.get('res_model') != 'ir.ui.menu'\
        and data.get('model') != 'ir.ui.menu' and not 'home_action' in data:
        action['target'] = 'popup'
        open_new_tab = True

    # search_view key in action is >8k added to the URL every time, which
    # breaks firefox (and probably Apache) as it's shoved into a header and
    # then used back as a URL
    action.pop('search_view', None)

    # when perform any button action on unsaved-record which returns 'ir.action.act_window'
    # which pop-up new window but 'appcontent' is not reloaded
    # for that passing active_id in headers, to get it in openAction
    if getattr(cherrypy.request, 'params', []):
        if getattr(cherrypy.request.params, 'context', {}):
            cherrypy.response.headers['active_id'] = cherrypy.request.params.context.get('active_id')

    # Add 'opened' mark to indicate we're now within the popup and can
    # continue on during the second round of execution
    payload = str({
      'action': dict(action, opened=True),
      'data': data
    })
    # Use compressed payloads in order to keep the URL under MSIE's size
    # limitations. Plus repeated urlencodings of serialized Python data
    # (or json) lead to a combinatorial explosion as there are very many
    # "special" characters which get urlencoded originally (thus several
    # times over). base64 strings are far less sensitive to this issue,
    # and immune when using urlsafe_b64encode
    compressed_payload = base64.urlsafe_b64encode(zlib.compress(payload))
    url = ('/openerp/execute?' +
           urllib.urlencode({'payload': compressed_payload}))

    if open_new_tab:
        parent_id = False
        if data['context'] and data['context'].get('active_id') and not data.get('model'):
            parent = rpc.RPCProxy('ir.ui.menu').read([int(data['context']['active_id'])],['complete_name'], rpc.session.context)[0]['complete_name'].split('/')[0]
            parent_id = rpc.RPCProxy('ir.ui.menu').search([('name','=', parent),('parent_id','=',False)],0,0,0, rpc.session.context)
        if parent_id:
            url = '/openerp/?' + urllib.urlencode({'active': parent_id[0],'next': url})
        else:
            url = '/openerp/?' + urllib.urlencode({'next': url})

    cherrypy.response.headers['X-Target'] = action['target']
    cherrypy.response.headers['Location'] = url
    return """<script type="text/javascript">
        window.top.openAction('%s', '%s');
    </script>
    """ % (url, action['target'])

def execute(action, **data):
    """Execute the action with the provided data. for internal use only.

    @param action: the action
    @param data: the data

    @return: mostly XHTML code
    """
    if 'type' not in action:
        #XXX: in gtk client just returns to the caller
        #raise common.error('Error', 'Invalid action...')
        return;

    data.setdefault('context', {}).update(expr_eval(action.get('context') or action.get('form_context', '{}'), data.get('context', {})))

    action_executor = ACTIONS_BY_TYPE[action['type']]
    return action_executor(action, data)

def execute_url(**data):
    url = data.get('url') or ''
    parsed = urlparse.urlsplit(url)
    if not (parsed.netloc or parsed.path.startswith('/')):
        raise common.message(_('Relative URLs are not supported'))

    if parsed.netloc:
        # external URL

        # determine target for openAction()
        target = {'new': 'popup'}.get(data['target'], 'iframe')

        return """<script type="text/javascript">
                      openAction('%s', '%s')
                  </script>
                """ % (url, target)

    return """<script type="text/javascript">
                  openLink('%s')
              </script>
            """ % url
    

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
    ctx = dict(data.get('context', {}), **rpc.session.context)
    if 'id' in data:
        try:
            id = data.get('id', False)
            if (id): id = int(id)
            actions = rpc.session.execute('object', 'execute', 'ir.values', 'get', 'action', keyword, [(data['model'], id)], False, ctx)
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
        key = keyact.keys()[0]
        if data.get('context'):
            data['context'].update(rpc.session.context)
        return execute(keyact[key], **data)
    else:
        return Selection().create(keyact, **data)


@tools.expose(template="/openerp/controllers/templates/closepopup.mako")
def close_popup(reload=True):
    """ Closes an opened dialog box or popup.

    :param reload: whether the background view should be reloaded when closing the popup
    :type reload: bool

    :return: the rendered popup-closing template
    :rtype: str
    """
    active_id = False
    if getattr(cherrypy.request, 'params', []):
        if getattr(cherrypy.request.params, 'context', {}):
            active_id = cherrypy.request.params.context.get('active_id')
    return {'reload': reload, 'active_id': active_id}

@tools.expose(template="/openerp/controllers/templates/report.mako")
def report_link(report_name, **kw):
    cherrypy.response.headers['X-Target'] = 'download'
    cherrypy.response.headers['Location'] = tools.url(
            '/openerp/report', report_name=report_name, **kw)
    return dict(name=report_name, data=kw)
    
