<%inherit file="/openobject/controllers/templates/base.mako"/>

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
                        <td width="100%">${_("Information")}</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                % if tmp and not message:
                <div class="box2">
                    <table border="0" width="100%" align="center">
                        % for key, val in todo:
                        <tr>
                            <td class="label" width="50%">${val}:</td>
                            <td width="50%">${tmp[key]}</td>
                        </tr>
                        % endfor
                    </table>
                </div>
                % endif
                % if message and not tmp:
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
                                <button type="button" onclick="window.close()">${_("OK")}</button>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</%def>
