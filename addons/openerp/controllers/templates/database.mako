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
</%def>

<%def name="content()">

<%include file="header.mako"/>

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
        <hr style="margin: 0 0 !important;">
        <div>${form.display()}</div>
    </div>
<%include file="footer.mako"/>    
</%def>
