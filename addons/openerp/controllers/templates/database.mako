<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>
<%def name="current_for(name)"><%
    if form.name == name: context.write('current')
%></%def>
<%def name="header()">
    <title>${form.string}</title>

    <script type="text/javascript" src="/openerp/static/javascript/openerp/openerp.ui.waitbox.js"></script>
    
    <link rel="stylesheet" type="text/css" href="/openerp/static/css/waitbox.css"/>
    <link rel="stylesheet" type="text/css" href="/openerp/static/css/database.css"/>

    <script type="text/javascript">
        function on_create() {
            new openerp.ui.WaitBox().showAfter(2000);
            return true;
        }
    </script>
    % if error:
        <script type="text/javascript">
            var $error_tbl = jQuery('<table class="errorbox">');
            $error_tbl.append('<tr><td style="padding: 4px 2px;" width="10%"><img src="/openerp/static/images/warning.png"></td><td class="error_message_content">${error["message"]}</td></tr>');
            $error_tbl.append('<tr><td style="padding: 0 8px 5px 0; vertical-align:top;" align="right" colspan="2"><a class="button-a" id="error_btn" onclick="$error_tbl.dialog(\'close\');">OK</a></td></tr>');

            jQuery(document).ready(function () {
                jQuery(document.body).append($error_tbl);
                $error_tbl.dialog({
                    modal: true,
                    resizable: false,
                    title: '<div class="error_message_header">${error.get("title", "Warning")}</div>'
                });
            })
        </script>
    % endif
</%def>

<%def name="content()">
	<table width="100%">
        <tr><%include file="header.mako"/></tr>
    </table>
    <div class="db-form">
        <div>
            <table width="100%" class="titlebar">
                <tr>
                    <td width="32px" align="center">
                        <img alt="" src="/openerp/static/images/stock/stock_person.png">
                    </td>
                    <td class="action">${form.string}</td>
                    <td class="links">
                        <a class="button static_boxes" href="${py.url('/')}">${_("Login")}</a>
                        <a class="button static_boxes ${current_for('create')}"
                           href="${py.url('/openerp/database/create')}">${_("Create")}</a>
                        <a class="button static_boxes ${current_for('drop')}"
                           href="${py.url('/openerp/database/drop')}">${_("Drop")}</a>
                        <a class="button static_boxes ${current_for('backup')}"
                           href="${py.url('/openerp/database/backup')}">${_("Backup")}</a>
                        <a class="button static_boxes ${current_for('restore')}"
                           href="${py.url('/openerp/database/restore')}">${_("Restore")}</a>
                        <a class="button static_boxes ${current_for('password')}"
                           href="${py.url('/openerp/database/password')}">${_("Password")}</a>
                    </td>
                </tr>
            </table>
        </div>
        <hr style="margin: 0 0 !important; background-color: #5A5858;">
        % if form.name == 'create':
            <div>${form.display(value=dict(password = "admin"))}</div>
        % else:
            <div>${form.display()}</div>
        % endif
    </div>
<%include file="footer.mako"/>    
</%def>
