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
            jQuery(document).ready(function () {

                var error_tbl = jQuery('<table class="errorbox" width="100%" height="100%">');
                error_tbl.append(jQuery('<tr><td class="error_message_header" colspan="2">${error.get("title", "Warning")}</td></tr>'));
                error_tbl.append(jQuery('<tr><td style="padding: 4px 2px;" width="10%"><img src="/openerp/static/images/warning.png"></img></td><td class="error_message_content">${error["message"]}</td></tr>'));
                error_tbl.append(jQuery('<tr><td style="padding: 0px 8px 5px 0px; vertical-align:top;" align="right" colspan="2"><a class="button-a" id="error_btn" onclick="jQuery.fancybox.close();">OK</a></td></tr>'));
                jQuery.fancybox({
                	content: error_tbl,
                	showCloseButton: false,
                	autoDimensions: true});
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
        <div>${form.display()}</div>
    </div>
<%include file="footer.mako"/>    
</%def>
