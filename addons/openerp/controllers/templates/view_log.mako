<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${_("Information")}</title>
    <link href="/openerp/static/css/style.css" rel="stylesheet" type="text/css"/>
</%def>

<%def name="content()">
    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="100%"><h1>${_("Information")}</h1></td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                % if not message:
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
                % else:
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td style="text-align: center;" width="100%">${message}</td>
                        </tr>
                    </table>
                </div><br/>
                % endif
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td width="100%">
                            </td>
                            <td>
                            	<a class="button-a" href="javascript: void(0)" onclick="window.close()">${_("OK")}</a>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</%def>
