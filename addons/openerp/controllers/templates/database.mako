<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>${form.string}</title>

    <script type="text/javascript" src="/openerp/static/javascript/openerp/openerp.ui.waitbox.js"></script>
    
    <link rel="stylesheet" type="text/css" href="/openerp/static/css/waitbox.css"/>
    <link rel="stylesheet" type="text/css" href="/openerp/static/css/database.css"/>

    <script type="text/javascript">

        var WAITBOX = null;

        MochiKit.DOM.addLoadEvent(function(evt){
            WAITBOX = new openerp.ui.WaitBox();
        });

        var dbView = function(name) {
            window.location.href = "${py.url('/openerp/database/')}" + name;
        }

        var on_create = function() {
            MochiKit.Async.callLater(2, function(){
                WAITBOX.show();
            });
            return true;
        }

    </script>
</%def>

<%def name="content()">

<%include file="header.mako"/>

    <table cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
            <td style="padding-top: 65px;" valign="top">
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
                                onclick="dbView('create')" class="static_buttons">${_("Create")}</button>
                            <button type="button" 
                                title="${_('Drop database')}"
                                ${py.disabled(form.name=='drop')}
                                onclick="dbView('drop')" class="static_buttons">${_("Drop")}</button>
                            <button type="button" 
                                title="${_('Backup database')}"
                                ${py.disabled(form.name=='backup')}
                                onclick="dbView('backup')" class="static_buttons">${_("Backup")}</button>
                            <button type="button" 
                                title="${_('Restore database')}"
                                ${py.disabled(form.name=='restore')}
                                onclick="dbView('restore')" class="static_buttons">${_("Restore")}</button>
                            <button type="button" 
                                title="${_('Change Administrator Password')}"
                                ${py.disabled(form.name=='password')}
                                onclick="dbView('password')" class="static_buttons">${_("Password")}</button>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td valign="top" align="center">${form.display()}</td>
        </tr>
    </table>
<%include file="footer.mako"/>    
</%def>
