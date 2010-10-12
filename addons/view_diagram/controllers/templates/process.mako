<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

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
            var id = parseInt(openobject.dom.get('select_workflow').value, 10) || null;
            var res_model = openobject.dom.get('res_model').value || null;
            var res_id = parseInt(openobject.dom.get('res_id').value, 10) || null;
            openLink(openobject.http.getURL("/view_diagram/process", {id: id, res_model: res_model, res_id: res_id, title: '${title}'}));
        }
    </script>
    % else:
    <script type="text/javascript">
        jQuery(document).ready(function(evt){

            var id = parseInt(openobject.dom.get('id').value, 10) || 0;
            var res_model = openobject.dom.get('res_model').value;
            var res_id = openobject.dom.get('res_id').value || 0;

            if (id) {
                var wkf = new openobject.process.Workflow('process_canvas');
                wkf.load(id, res_model, res_id, '${title}');
            }
        });
    </script>
    % endif
</%def>

<%def name="content()">
    <table class="view" border="0" width="100%" height="100%" cellpadding="0" cellspacing="0">
        <tr>
            <td width="75%" valign="top" style="padding-top:10px;">
                <h1>Help: ${title}</h1>
		        <div style="padding:5px 10px; min-height:56px;">
                    <p><i>${help}</i></p>
                </div>
            </td>
	    	<td width="25%" align="center" rowspan="4" valign="top">
                <div style="border-left: 2px solid; padding: 0 10px;">
                    <a class="help-button-a" target="_blank" href=" http://www.openerp.com/services/subscribe-onsite" style="padding-bottom:3px;">
                        ${_("Get the OpenERP Warranty %(by)s",
                        by="""<small>More on our Website</small>""")|n}
                    </a>
                    <a class="help-button-a" target="_blank" href="http://www.openerp.com/services/books" style="padding-bottom:3px;">
                        ${_("Get Books %(available)s",
                        available="""<small>Available in Amazon</small>""")|n}
                    </a>

                    <a class="help-button-a" target="_blank" href="http://www.openobject.com/forum">
                        ${_("Community Forum %(community)s",
                        community="""<small>Join Community Discussion</small>""")|n}
                    </a>
                </div>
            </td>
        </tr>

        <tr>
            <td style="text-align:right" valign="bottom">
                <a target="_blank" href="${context_help}" style="color:#9a0404; font-size:1.25em; font-weight:bold; font-style:italic"><u>${_("Online Documentation...")}</u></a>
            </td>
        </tr>

        <tr>
            <td style="padding-bottom:0" colspan="1" valign="bottom">
                <h2 style="padding:0 0 0 10px; font-weight:bold">${process_title} ${_("Process")}</h2>
            </td>
        </tr>

        % if selection:
        <tr>
            <td colspan="1">
                <input type="hidden" id="res_model" value="${res_model}"/>
                <input type="hidden" id="res_id" value="${res_id}"/>
                <fieldset style="margin: 0 0 10px 10px">
                    <legend><b style="padding: 4px;">${_("Select Process")}</b></legend>
                    <select id="select_workflow" name="select_workflow" style="min-width: 150px">
                        % for val, text in selection:
                        <option value="${val}" ${val==id and "selected" or ""} >${text}</option>
                        % endfor
                    </select>
                    <button class="button" type="button" onclick="select_workflow()">${_("Select")}</button>
                </fieldset>
            </td>
        </tr>

        %else:
        <tr>
            <td colspan="2">
                <input type="hidden" id="id" value="${id}"/>
                <input type="hidden" id="res_model" value="${res_model}"/>
                <input type="hidden" id="res_id" value="${res_id}"/>
                <div id="process_canvas" style="margin-top: 0"></div>
                <div align="left" style="padding: 5px 10px;">
                    <a target="_blank" id="show_customize_menu" href="${py.url('/openerp/form/edit', model='process.process', id=id)}">${_("[Edit Process]")}</a><br/>
                </div>
            </td>
        </tr>
        % endif

        % if fields:
        <tr>
            <td colspan="2">
                <h2 style="padding: 5px 10px; font-weight:bold">${_("Fields")} (model: ${res_model})</h2>
                <div align="left" style="padding: 5px 10px;">
                    <table border="0">
                    % for k, v in fields.items():
                        <tr>
                            <td valign="top">
                                <span class="process-field-name">${k}:</span>
                            </td>
                            <td valign="top">
                            % for l, m in v.items():
                                % if m:
                                    % if m == True:
                                        <span class="process-field-attribute-name">${l}</span>,<br />
                                    % else:
                                        <span class="process-field-attribute-name">${l}</span>: <span class="process-field-attribute-value">${m}</span>,<br />
                                    % endif
                                % endif
                            % endfor
                            </td>
                        </tr>
                        <tr>
                            <td valign="top" colspan="2">&nbsp;</td>
                        </tr>
                    % endfor
                    </table>
                </div>
            </td>
        </tr>
        % endif
    </table>
</%def>
