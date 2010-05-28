<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>${_("Process")}</title>
    <link type="text/css" rel="stylesheet" href="/view_diagram/static/css/process.css"/>

    <script src="/view_diagram/static/javascript/draw2d/wz_jsgraphics.js"></script>
    <script src="/view_diagram/static/javascript/draw2d/mootools.js"></script>
    <script src="/view_diagram/static/javascript/draw2d/moocanvas.js"></script>
    <script src="/view_diagram/static/javascript/draw2d/draw2d.js"></script>

    <script src="/view_diagram/static/javascript/process.js"></script>

    <script type="text/javascript">
        var context_help = function() {
            return window.open(openobject.http.getURL('http://doc.openerp.com/index.php', {model: 'process.process', lang:'${rpc.session.context.get('lang', 'en')}'}));
        }
    </script>

    % if selection:
    <script type="text/javascript">
        var select_workflow = function() {
            var id = parseInt(openobject.dom.get('select_workflow').value) || null;
            var res_model = openobject.dom.get('res_model').value || null;
            var res_id = parseInt(openobject.dom.get('res_id').value) || null;
            window.location.href = openobject.http.getURL("/view_diagram/process", {id: id, res_model: res_model, res_id: res_id});
        }
    </script>
    % endif
</%def>

<%def name="content()">

% if selection:
<div class="view">
    <input type="hidden" id="res_model" value="${res_model}"/>
    <input type="hidden" id="res_id" value="${res_id}"/>
    <fieldset>
        <legend><b>${_("Select Process")}</b></legend>
        <select id="select_workflow" name="select_workflow" style="min-width: 150px">
            % for val, text in selection:
            <option value="${val}">${text}</option>
            % endfor
        </select>
        <button class="button" type="button" onclick="select_workflow()">${_("Select")}</button>
    </fieldset>
</div>
% else:
<table class="view" width="100%" border="0" cellpadding="0" cellspacing="0">
    <tr>
        <td width="100%" valign="top">
            <table width="100%" class="titlebar">
                <tr>
                    <td width="32px" align="center">
                        <img src="/openerp/static/images/stock/gtk-refresh.png"/>
                    </td>
                    <td width="100%" id="process_title">${title}</td>
                    <td nowrap="nowrap">
                        <img class="button" title="${_('Help')}" src="/openerp/static/images/stock/gtk-help.png" width="16" height="16"
                        onclick="context_help()"/>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <input type="hidden" id="id" value="${id}"/>
            <input type="hidden" id="res_model" value="${res_model}"/>
            <input type="hidden" id="res_id" value="${res_id}"/>
            <div id="process_canvas"></div>
            <script type="text/javascript">
                var id = parseInt(openobject.dom.get('id').value, 10) || 0;
                var res_model = openobject.dom.get('res_model').value;
                var res_id = openobject.dom.get('res_id').value;
                
                if (id) {
                    var wkf = new openobject.process.Workflow('process_canvas');
                    wkf.load(id, res_model, res_id);
                }                 
            </script>
        </td>
    </tr>
    <tr>
        <td class="dimmed-text">
            [<a target="_blank" href="${py.url('/openerp/form/edit', model='process.process', id=id)}">${_("Customize")}</a>]
        </td>
    </tr>
</table>
%endif


</%def>
