<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${form.string}</title>

    <script type="text/javascript" src="/openerp/static/javascript/openerp/openerp.ui.waitbox.js"></script>
    
    <link rel="stylesheet" type="text/css" href="/openerp/static/css/waitbox.css"/>
    <link rel="stylesheet" type="text/css" href="/openerp/static/css/database.css"/>

    <script type="text/javascript">

        var WAIT_BOX = null;

        jQuery(document).ready(function(){
            WAIT_BOX = new openerp.ui.WaitBox();
        });

        var dbView = function(name) {
            window.location.href = "${py.url('/openerp/database/')}" + name;
        };

        var on_create = function() {
            WAIT_BOX.showAfter(2000);
            return true;
        }

    </script>
</%def>

<%def name="content()">

<%include file="header.mako"/>

    <table cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
            <td valign="top" style="padding: 0px;">
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/openerp/static/images/stock/stock_person.png"/>
                        </td>
                        <td class="db_action_string" width="100%">${form.string}</td>
                        <td nowrap="nowrap">
                            <button type="button" 
                                title="${_('Create database')}"
                                ${py.disabled(form.name=='create')}
                                onclick="dbView('create')" class="static_boxes">${_("Create")}</button>
                            <button type="button" 
                                title="${_('Drop database')}"
                                ${py.disabled(form.name=='drop')}
                                onclick="dbView('drop')" class="static_boxes">${_("Drop")}</button>
                            <button type="button" 
                                title="${_('Backup database')}"
                                ${py.disabled(form.name=='backup')}
                                onclick="dbView('backup')" class="static_boxes">${_("Backup")}</button>
                            <button type="button" 
                                title="${_('Restore database')}"
                                ${py.disabled(form.name=='restore')}
                                onclick="dbView('restore')" class="static_boxes">${_("Restore")}</button>
                            <button type="button" 
                                title="${_('Change Administrator Password')}"
                                ${py.disabled(form.name=='password')}
                                onclick="dbView('password')" class="static_boxes">${_("Password")}</button>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
        	<td style="padding: 0px;"><hr style="margin: 0 0 !important;"/></td>
        </tr>
        <tr>
            <td valign="top" align="center">${form.display()}</td>
        </tr>
    </table>
<%include file="footer.mako"/>    
</%def>
