<%inherit file="master.mako"/>

<%def name="header()">
    <title>Login</title>
</%def>

<%def name="content()">
    <div class="view">

        <br/>

        <center>
            <img src="/static/images/developped_by.png" border="0" width="200" height="60" alt="${_('Developped by Axelor and Tiny')}"/>
        </center>

        <br/>

        <form action="${target}" method="post" name="loginform">
            % for key, value in origArgs.items():
            <input type="hidden" name="${key}" value="${str(value)}"/>
            % endfor
            <input type="hidden" name="login_action" value="login"/>
        
            <div class="box2 welcome">Welcome to OpenERP</div>

            <div class="box2">
                <table align="center" cellspacing="2px" border="0">
                    % if dblist is not None:
                    <tr>
                        <td class="label">
                            <span>Server:</span>
                        </td>
                        <td>${url}</td>
                    </tr>
                    <tr>
                        <td class="label">Database:</td>
                        <td>
                            <select name="db" style="width: 302px;">
                                % for v in dblist or []:
                                <option value="${v}" ${v==db and "selected" or ""}>${v}</option>
                                % endfor
                            </select>
                        </td>
                    </tr>
                    % endif

                    <tr>
                        <td class="label">User:</td>
                        <td><input type="text" id="user" name="user" style="width: 300px;" value="${user}"/></td>
                    </tr>
                    
                    <tr>
                        <td class="label">Password:</td>
                        <td><input type="password" value="${password or ''}" id="password" name="password" style="width: 300px;"/></td>
                    </tr>
                    <tr>
                        <td></td>
                        <td align="right">
                            % if cp.config('dbbutton.visible', 'openerp-web'):
                            <button type="button" style="white-space: nowrap" tabindex="-1" onclick="location.href='/database'">Databases</button>
                            % endif
                            <button type="submit" style="width: 80px; white-space: nowrap">Login</button>
                        </td>
                    </tr>
                </table>                
            </div>            
        </form>

        % if message:
        <div class="box2 message" id="message">${message}</div>
        % endif
    </div>
</%def>
