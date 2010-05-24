<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>${_("Login")}</title>
</%def>

<%def name="content()">

<%include file="header.mako"/>

    <div class="view" style="padding-top: 90px;">

        <form action="${py.url(target)}" method="post" name="loginform">
            % for key, value in origArgs.items():
            <input type="hidden" name="${key}" value="${value}"/>
            % endfor
            <input type="hidden" name="login_action" value="login"/>
        
            <div class="box2 welcome-message">${_("Welcome to OpenERP")}</div>

            <div class="box2">
                <table align="center" cellspacing="2px" border="0">
                    <tr>
                        <td class="label"><label for="db">${_("Database:")}</label></td>
                        <td>
                            % if dblist is None:
                                <input type="text" name="db" id="db" style="width: 300px;" value="${db}"/>
                            % else:
                            <select name="db" id="db" style="width: 302px;">
                                % for v in dblist:
                                <option value="${v}" ${v==db and "selected" or ""}>${v}</option>
                                % endfor
                            </select>
                            % endif
                        </td>
                    </tr>

                    <tr>
                        <td class="label"><label for="user">${_("User:")}</label></td>
                        <td><input type="text" id="user" name="user" style="width: 300px;" value="${user}"/></td>
                    </tr>
                    
                    <tr>
                        <td class="label"><label for="password">${_("Password:")}</label></td>
                        <td><input type="password" value="${password}" id="password" name="password" style="width: 300px;"/></td>
                    </tr>
                    <tr>
                        <td></td>
                        <td style="text-align: right; padding-right: 55px;">
                            % if cp.config('dbbutton.visible', 'openobject-web'):
	                            <button type="button" class="static_buttons" tabindex="-1" onclick="location.href='${py.url('/openerp/database')}'">${_("Databases")}</button>
                            % endif
                            <button type="submit" class="static_buttons">${_("Login")}</button>
                        </td>
                    </tr>
                </table>                
            </div>            
        </form>
    
        % if message:
        <div class="box2 message" id="message">${message}</div>
        % endif
        
        % if info:
        <div class="information">${info|n}</div>
        % endif
    </div>
<%include file="footer.mako"/>    
</%def>
