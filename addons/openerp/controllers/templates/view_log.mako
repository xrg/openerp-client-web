<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${_("Information")}</title>
    <link href="/openerp/static/css/style.css" rel="stylesheet" type="text/css"/>
</%def>

<%def name="content()">
    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td align="center" style="padding: 10px 0 0 0;">
                <table>
                    <tr>
                        <td class="popup_header" style="padding: 0px; width: 470px;">${_("Information")}</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td style="padding: 0px;">
                <div class="box2">
                    <table border="0" width="100%" align="center">
                        % for field, description in fields:
                        <tr>
                            <td class="label" width="50%">${description}:</td>
                            <td width="50%">${values[field]}</td>
                        </tr>
                        % endfor
                    </table>
                </div>
                <div class="toolbar" align="center">
                    <table border="0" cellpadding="0" cellspacing="0">
                        <tr>
                            <td class="popup_footer" style="width: 450px;">
                            	<a class="button-a" style="float: right;" href="javascript: void(0)" onclick="window.close()">${_("OK")}</a>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</%def>
