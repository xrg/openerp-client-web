<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>
<%!
    MAINTENANCE_CONTRACTS_URL = 'http://www.openerp.com/support-or-publisher-warranty-contract'
%>
<%def name="header()">
    <script type="text/javascript" src="/openerp/static/javascript/openerp/openerp.ui.textarea.js"></script>

    <script type="text/javascript">
        % if maintenance:
        var send_maintenance_request = function() {
            var args = {
                explanation: openobject.dom.get('explanation').value,
                remarks: openobject.dom.get('remarks').value,
                name: openobject.dom.get('issue_name').value,
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
            jQuery('.error-section h5[id!="non-fold-error-link"]').click(function () {
                jQuery(this).parent().toggleClass('expanded-error collapsed-error');
            });
        });
        % endif
        function close_error_window() {
            if (jQuery('div#fancybox-wrap').is(':visible')) {
                % if all_params and all_params.get('_terp_id'):
                    if(jQuery('#_terp_ids').length) {
                        jQuery('#_terp_ids').val('${all_params.get('_terp_ids')}')
                        jQuery('#_terp_id').val('${all_params.get('_terp_id')}')
                    }
                % endif
                jQuery.fancybox.close();
                return;
            }

            var topWindow;
            if(window.top != window) {
                topWindow = window.top;
            } else {
                topWindow = window.opener;
            }
            var $doc = jQuery(topWindow.document);
            var terp_id = jQuery(idSelector('_terp_id'), $doc).val();

            var frame_element;
            if(jQuery(window).attr('frameElement')) {
               frame_element = window.frameElement;
            } else {
               frame_element = jQuery.fancybox;
            }

            if (terp_id) {
                frame_element.close();
                return;
            }

            if (history.length > 1) {
                history.back();
                frame_element.close();
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
                        <h4 style="padding-top:10px;">${_("An %(error_type)s has been reported.", error_type=title)}</h4>
                        <div class="error-section collapsed-error">
                            <h5><label for="error">${_('Let me fix it')}</label></h5>
                            <div class="details">
                                <textarea id="error" name="error" class="text" readonly="readonly" rows="15" >${error}</textarea>
                            </div>
                        </div>
                        <div class="error-section ${maintenance_default}">
                            % if maintenance['status'] != 'full':
                            <h5 id="non-fold-error-link"><a href="${MAINTENANCE_CONTRACTS_URL}" target="_blank">${_('Fix it for me')}</a></h5>
                            % else:
                            <h5>${_('Fix it for me')}</h5>
                            <div class="details">
                                <div>
                                    <table width="100%">
                                        <tr>
                                            <td colspan="2" align="center">
                                                <strong>${_("Publisher warranty contract.")}</strong><br/><br/>
                                                <em>${_("Your request will be sent to OpenERP and publisher warranty team will reply you shortly.")}</em>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td class="label"><label for="issue_name">${_("Summary of the problem:")}</label></td>
                                            <td class="item">
                                                <input type="text" id="issue_name" name="issue_name" class="text"></input>
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
                                                    ${_("Send to Publisher Warranty Team")}
                                                </button>
                                            </td>
                                        </tr>
                                    </table>
                                </div>
                            </div>
                            % endif
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
