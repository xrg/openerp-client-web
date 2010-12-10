<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>
<%!
    MAINTENANCE_CONTRACTS_LINK = '<a href="http://www.openerp.com/" target="_blank">See more about maintenance contracts.</a>'
%>
<%def name="header()">
    <script type="text/javascript" src="/openerp/static/javascript/openerp/openerp.ui.textarea.js"></script>

    <script type="text/javascript">
        % if maintenance:
        var send_maintenance_request = function() {
            var args = {
                explanation: openobject.dom.get('explanation').value,
                remarks: openobject.dom.get('remarks').value,
                tb: openobject.dom.get('error').value
            };

            var req = openobject.http.postJSON('/openerp/errorpage/submit', args);

            req.addCallback(function(obj) {

                if (obj.error) {
                    return error_display(obj.error);
                }

                if (obj.message) {
                    error_display(obj.message)
                }

                history.length > 1 ? history.back() : window.close()
            });
            return false;
        };

        jQuery(document).ready(function () {
            new openerp.ui.TextArea('error');
            jQuery('.error-section h5').click(function () {
                jQuery(this).parent().toggleClass('expanded-error collapsed-error');
            });
        });
        % endif
        function close_error_window() {
            if (jQuery('div#fancybox-wrap').is(':visible')) {
                % if all_params and all_params.get('_terp_id'):
                    if(jQuery('#_terp_ids').length) {
                        jQuery('#_terp_ids').val('${all_params.ids}')
                        jQuery('#_terp_id').val('${all_params.id}')
                    }
                % endif
                jQuery.fancybox.close();
                return;
            }
            if (history.length > 1) {
                history.back()
            } else {
                window.close();
            }
        }
    </script>
</%def>

<%def name="content()">

<table class="view" border="0" width="100%">
    <tr>
        % if maintenance:
            <%
                if maintenance['status'] == 'full':
                    maintenance_default = 'expanded-error'
                else:
                    maintenance_default = 'collapsed-error'
            %>

            <td valign="top">
                <form id="view_form" action="/openerp/errorpage/submit" method="POST">
                    <div>
                        <h4 style="padding-top:10px;">${_("An ")} ${'%s' % title} ${_("has been reported.")}</h4>
                        <div class="error-section collapsed-error">
                            <h5><label for="error">${_('Let me fix it')}</label></h5>
                            <div class="details">
                                <textarea id="error" name="error" class="text" readonly="readonly" rows="20" >${error}</textarea>
                            </div>
                        </div>
                        <div class="error-section ${maintenance_default}">
                            <h5>${_('Fix it for me')}</h5>
                            <div class="details">
                                % if maintenance['status'] == 'none':
                                <pre>

<b>${_("You do not have a valid OpenERP maintenance contract !")}</b><br/><br/>
${_("""If you are using OpenERP in production, it is recommended to have
a maintenance program.

The OpenERP maintenance contract provides you with bug fix guarantees and an
automatic migration system so that we can start working on your problems within a few
hours.

With a maintenance contract, errors such as this one can be sent directly to the OpenERP
team for review and evaluation.

The maintenance program offers you:
* Automatic migrations on new versions,
* A bugfix guarantee,
* Monthly announces of potential bugs and their fixes,
* Security alerts by email and automatic migration,
* Access to the customer portal.
""")}
${MAINTENANCE_CONTRACTS_LINK|n}
                                </pre>
                                % elif maintenance['status'] == 'partial':
                                <pre>

${_("""Your maintenance contract does not cover all modules installed in your system !
If you are using OpenERP in production, it is highly suggested to upgrade your
contract.

If you have developed your own modules or installed third party module, we
can provide you an additional maintenance contract for these modules. After
having reviewed your modules, our quality team will ensure they will migrate
automatically for all future stable versions of OpenERP at no extra cost.

Here is the list of modules not covered by your maintenance contract:""")}

% for mod in maintenance['uncovered_modules']:
${' * %s\n' % mod}
% endfor

${MAINTENANCE_CONTRACTS_LINK|n}
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
                                                <textarea id="explanation" name="explanation" class="text"></textarea>
                                                <script type="text/javascript">
                                                    new openerp.ui.TextArea('explanation');
                                                </script>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td class="label"><label for="remarks">${_("Other Comments:")}</label></td>
                                            <td class="item">
                                                <textarea id="remarks" class="text" name="remarks"></textarea>
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
            <td valign="top" style="padding: 0px;">
                % if concurrency:
                    <form action="${target}" method="post" name="error_page" enctype="multipart/form-data">
                            % for key, value in all_params.items():
                            % if key != '_terp_concurrency_info':
                                <input type="hidden" name="${key}" value="${value}"/>
                            % endif
                        % endfor

                        <table class="errorbox" align="center">
                            <tr>
                                <td height="15px"></td>
                            </tr>
                            <tr>
                                <td class="error_message_header">${_("Write concurrency warning :")}</td>
                            </tr>
                            <tr>
                                <td style="padding: 30px;">
                                <pre>
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
                                       onclick="close_error_window()">${_("Cancel")}</a>
                                    <button type="submit" onclick="close_error_window()">${_("Write Anyway")}</button>
                                </td>
                            </tr>
                        </table>
                    % else:
                        <table class="errorbox" align="center">
                            <tr>
                                <td colspan="2" class="error_message_header">${title}</td>
                            </tr>
                            <tr>
                                <td style="padding: 4px 2px;">
                                	<img src="/openerp/static/images/warning.png"></img>
                                </td>
                                <td class="error_message_content">${error}</td>
                            </tr>
                            <tr>
                                <td colspan="2" align="right" style="padding: 1px">
                                    <a class="button-a" href="javascript: void(0)"
                                       onclick="close_error_window()">OK</a>
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
