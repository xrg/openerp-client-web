<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <link href="/openerp/static/css/style.css" rel="stylesheet" type="text/css"/>

    <script type="text/javascript" src="/openerp/static/javascript/openerp/openerp.ui.textarea.js"></script>

    <script type="text/javascript">
        var send_maintenance_request = function() {
            var args = {
                explanation: openobject.dom.get('explanation').value,
                remarks: openobject.dom.get('remarks').value,
                tb: openobject.dom.get('error').value
            };

            var req = openobject.http.postJSON('/openerp/errorpage/submit', args);

            req.addCallback(function(obj) {

                if (obj.error) {
                    return alert(obj.error);
                }

                if (obj.message) {
                    alert(obj.message)
                }

                history.length > 1 ? history.back() : window.close()
            });
            return false;
        }
        
        function toggle_error(){
            var error = openobject.dom.get('traceback_details')
            
            error.style.display = error.style.display == "none" ? "" : "none";
            if (error.style.display == "none") {
                jQuery('#toggle-error').toggleClass('expand-error collapse-error')
            }
            else {
                jQuery('#toggle-error').toggleClass('collapse-error expand-error')
            }
        }
        
        function toggle_maintenance(){
            var maintenance = openobject.dom.get('maintenance_details')
            
            if (getNodeAttribute(maintenance, 'class') == "close"){
                jQuery('#toggle-maintenance').toggleClass('expand-error collapse-error')
                jQuery('#maintenance_details').toggleClass('close open')
            }
            else {
                jQuery('#toggle-maintenance').toggleClass('collapse-error expand-error ')
                jQuery('#maintenance_details').toggleClass('open close')
            }
        }
    </script>
</%def>

<%def name="content()">
<%
    if maintenance['status'] == 'full':
        a_class = "collapse-error"
        div_class = "open"
    else:
        a_class = "expand-error"
        div_class = "close"
%>

<table class="view" border="0" width="100%">
    <tr>
        % if maintenance:
            <td valign="top">
                <form id="view_form" action="/openerp/errorpage/submit" method="POST">
                    <div id="error_page_notebook">
                        <b>${_("An ")} ${'%s' % title} ${_("has been reported.")}</b><br/>
                        <div title="${_('Let me fix it !')}" style="margin-top:5px; padding-top:5px;">
                            <a class="expand-error" id="toggle-error" href="javascript: void(0)" onclick="toggle_error();">${_('[ Let me fix it! ]')}</a>
                            <div id="traceback_details" style="display:none; emargin-top:5px; padding-top:5px;">
                                <textarea id="error" name="error" class="text" readonly="readonly" style="width: 99%;" rows="20" >${error}</textarea>
                                <script type="text/javascript" title="${_('Application Error!')}">
                                    new openerp.ui.TextArea('error');
                                </script>
                            </div>
                        </div>
                        <div title="${_('Fix it for me !')}" style="margin-top:5px; padding-top:5px;">
                        <a class="${a_class}" id="toggle-maintenance" href="javascript: void(0)" onclick="toggle_maintenance('${maintenance['status']}');">${_('[ Fix it for me! ]')}</a>
                        <div title="${_('Maintenance')}" id="maintenance_details" class="${div_class}">
                            % if maintenance['status'] == 'none':
                                <pre>
<b>${_("An unknown error has been reported.")}</b><br/>

<b>${_("You do not have a valid Open ERP maintenance contract !")}</b><br/><br/>
${_("""If you are using Open ERP in production, it is highly suggested to subscribe
a maintenance program.

The Open ERP maintenance contract provides you a bugfix guarantee and an
automatic migration system so that we can fix your problems within a few
hours. If you had a maintenance contract, this error would have been sent
to the quality team of the Open ERP editor.

The maintenance program offers you:
* Automatic migrations on new versions,
* A bugfix guarantee,
* Monthly announces of potential bugs and their fixes,
* Security alerts by email and automatic migration,
* Access to the customer portal.

You can use the link bellow for more information. The detail of the error
is displayed on the second tab.""")}
<a href="http://www.openerp.com/" target="_blank">Click here for details about the maintenance proposition</a>
                                </pre>
                            % elif maintenance['status'] == 'partial':
                                <pre>

${_("""Your maintenance contract does not cover all modules installed in your system !
If you are using Open ERP in production, it is highly suggested to upgrade your
contract.

If you have developped your own modules or installed third party module, we
can provide you an additional maintenance contract for these modules. After
having reviewed your modules, our quality team will ensure they will migrate
automatically for all futur stable versions of Open ERP at no extra cost.

Here is the list of modules not covered by your maintenance contract:""")}

% for mod in maintenance['uncovered_modules']:
${' * %s\n' % mod}
% endfor
${_("""You can use the link bellow for more information.""")}
<a href="http://www.openerp.com/" target="_blank">Click here for details about the maintenance proposition</a>
                                </pre>
                            % elif maintenance['status'] == 'full':
                                <div>
                                    <table width="100%">
                                        <tr>
                                            <td colspan="2" align="center">
                                                <strong>${_("Maintenance contract.")}</strong><br/><br/>
                                                <em>${_("Your request will be sent to OpenERP and maintenance team will reply you shortly.")}</em>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td class="label" width="5%" nowrap="nowrap"><label for="explanation">
                                                ${_("Explain what you did:")}</label></td>
                                            <td class="item">
                                                <textarea id="explanation" name="explanation" class="text" rows="10"></textarea>
                                                <script type="text/javascript">
                                                    new openerp.ui.TextArea('explanation');
                                                </script>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td class="label"><label for="remarks">${_("Other Comments:")}</label></td>
                                            <td class="item">
                                                <textarea id="remarks" class="text" name="remarks" rows="10"></textarea>
                                                <script type="text/javascript">
                                                    new openerp.ui.TextArea('remarks');
                                                </script>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td></td>
                                            <td>
                                                <button onclick="return send_maintenance_request();">
                                                    ${_("Send to Maintenance Team")}
                                                </button>
                                            </td>
                                        </tr>
                                    </table>
                                </div>
                            % endif
                        </div>                        
                      </div>
                    </div>                   
                </form>
            </td>
        % else:
            <td valign="top">
                % if concurrency:
                    <form action="${target}" method="post" name="error_page" enctype="multipart/form-data">
                            % for key, value in all_params.items():
                            % if key != '_terp_concurrency_info':
                                <input type="hidden" name="${key}" value="${value}"/>
                            % endif
                        % endfor

                        <table border="0" cellpadding="0" cellspacing="0" align="center">
                            <tr>
                                <td height="15px"></td>
                            </tr>
                            <tr>
                                <td class="errorbox" style="padding: 30px;">
                                    <pre>
<b>${_("Write concurrency warning :")}</b><br/>
${_("""This document has been modified while you were editing it.
Choose:

    - "Cancel" to cancel saving.
    - "Write anyway" to save your current version.""")}
                                    </pre>
                                </td>
                            </tr>
                            <tr>
                                <td height="5px"></td>
                            </tr>
                            <tr>
                                <td class="errorbox" align="right">
                                    <a class="button-a" href="javascript: void(0)"
                                       onclick="history.length > 1 ? history.back() : window.close()">${_("Cancel")}</a>
                                    <button type="submit">${_("Write Anyway")}</button>
                                </td>
                            </tr>
                        </table>
                    % else:
                        <table border="0" cellpadding="0" cellspacing="0" align="center">
                            <tr>
                                <td height="15px"></td>
                            </tr>
                            <tr>
                                <td class="errorbox welcome">${title}</td>
                            </tr>
                            <tr>
                                <td height="5px"></td>
                            </tr>
                            <tr>
                                <td class="errorbox" style="padding: 30px;">
                                    <pre>${error}</pre>
                                </td>
                            </tr>
                            <tr>
                                <td height="5px"></td>
                            </tr>
                            <tr>
                                <td class="errorbox" align="right">
                                    <a class="button-a" href="javascript: void(0)"
                                       onclick="history.length > 1 ? history.back() : window.close()">OK</a>
                                </td>
                            </tr>
                        </table>
                    </form>
                % endif
            </td>
        % endif
    </tr>
</table>

</%def>
