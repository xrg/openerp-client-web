<%inherit file="../../templates/master.mako"/>

<%def name="header()">
    <link href="/static/css/style.css" rel="stylesheet" type="text/css" />
    <title>${title}</title>

    <script type="text/javascript" src="/static/javascript/textarea.js"></script>
    
    <script type="text/javascript">
        var send_maintenance_request = function() {

            var args = {
                explanation: getElement('explanation').value,
                remarks: getElement('remarks').value,
                tb: getElement('error').value
            }

            var req = Ajax.JSON.post('/errorpage/submit', args);

            req.addCallback(function(obj){

                if (obj.error) {
                    return alert(obj.error);
                }
                
                if (obj.message) {
                    alert(obj.message)
                }

                return history.length > 1 ? history.back() : window.close()
            });
        }
    </script>
</%def>

<%def name="content()">
     <table class="view" border="0" width="100%">
        % if maintenance:
        <tr>
            <td valign="top">
<form id="view_form" onsubmit="return false;">
                <div class='tabber' id="error_page_notebook">
                    <div class='tabbertab' title="Maintenance">
                            % if maintenance['status'] == 'none':
                            <pre>
<b>An unknown error has been reported.</b><br/>

<b>You do not have a valid Open ERP maintenance contract !</b><br/><br/>
If you are using Open ERP in production, it is highly suggested to subscribe
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
is displayed on the second tab.
                            </pre>
                            % elif maintenance['status'] == 'partial':
                            <pre>
<b>An unknown error has been reported.</b><br/><br/>

Your maintenance contract does not cover all modules installed in your system !
If you are using Open ERP in production, it is highly suggested to upgrade your
contract.

If you have developped your own modules or installed third party module, we
can provide you an additional maintenance contract for these modules. After
having reviewed your modules, our quality team will ensure they will migrate
automatically for all futur stable versions of Open ERP at no extra cost.

Here is the list of modules not covered by your maintenance contract:

% for mod in maintenance['uncovered_modules']:
${' * %s\n' % mod}
% endfor
You can use the link bellow for more information. The detail of the error
is displayed on the second tab.
                            </pre>
                            % elif maintenance['status'] == 'full':
                            <div>
                                <table width="100%">
                                    <tr>
                                        <td colspan="2" align="center">
                                            <strong>Maintenance contract.</strong><br/><br/>
                                            <em>Your request will be sent to OpenERP and maintenance team will reply you shortly.</em>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="label" width="5%" nowrap="nowrap">Explain what you did:</td>
                                        <td class="item">
                                            <textarea id="explanation" class="text" rows="10"/>
                                            <script type="text/javascript">
                                                new ResizableTextarea('explanation');
                                            </script>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="label">Other Comments:</td>
                                        <td class="item">
                                            <textarea id="remarks" class="text" rows="10"/>
                                            <script type="text/javascript">
                                                new ResizableTextarea('remarks');
                                            </script>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td></td>
                                        <td>
                                            <button class="button" type="button" onclick="send_maintenance_request()">Send to Maintenance Team</button>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                            % endif
                    </div>
                    <div class='tabbertab' title="Application Error!">
                        <textarea id="error" class="text" readonly="readonly" style="width: 99%" rows="20">${error}</textarea>
                        <script type="text/javascript">
                            new ResizableTextarea('error');
                        </script>
                    </div>
                </div>
                <script type="text/javascript">
                    tabberOptions.div = getElement('error_page_notebook');
                    tabberOptions.div.tabber = new tabberObj(tabberOptions);
                </script>
</form>
            </td>
        </tr>
        % else:
            <td valign="top">
                <table border="0" cellpadding="0" cellspacing="0" align="center">
                    <tr><td height="15px"/></tr>
                    <tr>
                        <td class="errorbox welcome">${title}</td>
                    </tr>
                    <tr><td height="5px"/></tr>
                    <tr>
                        <td class="errorbox" style="padding: 30px;">
                            <pre>${error}</pre>
                        </td>
                    </tr>
                    <tr><td height="5px"/></tr>
                    <tr>
                        <td class="errorbox" align="right">
                            <button type="button" onclick="history.length > 1 ? history.back() : window.close()">OK</button>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        % endif
    </table>
</%def>
