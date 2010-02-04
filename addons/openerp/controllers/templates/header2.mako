<%
# put in try block to prevent improper redirection on connection refuse error
try:
    ROOT = cp.request.pool.get_controller("/")
    SHORTCUTS = cp.request.pool.get_controller("/shortcuts")
    REQUESTS = cp.request.pool.get_controller("/requests")
    
    shortcuts = SHORTCUTS.my()
    requests, requests_message = REQUESTS.my()
except:

    ROOT = None
    
    shortcuts = []
    requests = []
    requests_message = None
%>

<table id="header" class="header" cellpadding="0" cellspacing="0" border="0">
    <tr>
        <td rowspan="2">
        <img src="/openerp/static/images/openerp_big.png" 
            alt="OpenERP" border="0" width="200px" height="60px" usemap="#logo_map"/>
            <map name="logo_map">
                <area shape="rect" coords="102,42,124,56" href="http://openerp.com" target="_blank"/>
                <area shape="rect" coords="145,42,184,56" href="http://axelor.com" target="_blank"/>
            </map>
        </td>
        <td align="right" valign="top" nowrap="nowrap" height="24">
            <table class="menu_connection" cellpadding="0" cellspacing="0" border="0">
                <tr>
                    <td>
                        <a href="http://openerp.com" target="_blank" title="OpenERP - Open Source Management Solution" style="padding: 0px;">
                            <img src="/openerp/static/images/openerp_small.png" border="0" width="86" height="24"/></a>
                    </td>
                    <td width="26" class="menu_connection_right" nowrap="nowrap">
                        <div style="width: 26px;"/>
                    </td>
                    <td class="menu_connection_welcome" nowrap="norwap">
                        ${_("Welcome %(user)s", user=rpc.session.user_name or 'guest')}
                    </td>
                    <td class="menu_connection_links" nowrap="norwap">
                        <a href="${py.url('/')}">${_("Home")}</a>
                        <a href="${py.url('/pref/create')}">${_("Preferences")}</a>
                        <a href="${py.url('/about')}">${_("About")}</a>
                        <a href="${py.url('/logout')}" target="_top">${_("Logout")}</a>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        % if rpc.session.is_logged():
        <td align="right" valign="middle" style="padding-right: 4px;">
            ${_("Requests:")} <a href="${py.url('/requests')}">${requests_message}</a>
        </td>
        % endif
    </tr>
</table>
