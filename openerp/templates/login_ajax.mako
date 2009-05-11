<%inherit file="master.mako"/>
<%! show_header_footer = False %>
<%def name="header()">
    <title>Login</title>

    <script type="text/javascript">

        var do_login = function(form) {

            if (Ajax.COUNT > 0) {
                return false;
            }

            var user = $('user').value;
            var password = $('password').value;

            if (!(user || password)) {
                MochiKit.Visual.Highlight('user', {'startcolor': '#FF6666'});
                MochiKit.Visual.Highlight('password', {'startcolor': '#FF6666'});
                $('user').focus();
                MochiKit.Style.hideElement('message');
                return false;
            }

            if (!user) {
                MochiKit.Visual.Highlight('user', {'startcolor': '#FF6666'});
                $('user').focus();
                MochiKit.Style.hideElement('message');
                return false;
            }

            if (!password) {
                MochiKit.Visual.Highlight('password', {'startcolor': '#FF6666'});
                $('password').focus();
                MochiKit.Style.hideElement('message');
                return false;
            }

            var req = Ajax.JSON.get('/login', {
                'db': $('db').value,
                'user': user,
                'password': password,
                'tg_format': 'json'
            });

            req.addCallback(function(obj){
                if (obj.result) {
                    $('password').value = '';
                    window.open($('location').value || '/');
                    MochiKit.Style.hideElement('message');
                } else {
                    MochiKit.Visual.appear('message');
                }
            });

            return false;
        }

    </script>
</%def>

<%def name="content()">
    <div class="view">

        <form onsubmit="return do_login()" action="/" method="post" name="loginform">
            <input type="hidden" id="location" name="location" value="${location}"/>
            <input type="hidden" id="db" name="db" value="${db}"/>

            % if style=='ajax_small':
            <table align="center" border="0">
                <tr>
                    <td><strong>${_("User:")}</strong></td>
                </tr>
                <tr>
                    <td><input type="text" id="user" name="user" style="width: 150px;" value="${user}"/></td>
                </tr>
                <tr>
                    <td><strong>${_("Password:")}</strong></td>
                </tr>
                <tr>
                    <td><input type="password" value="${password}" id="password" name="password" style="width: 150px;"/></td>
                </tr>
                <tr>
                    <td>
                        <button type="submit" style="width: 80px; white-space: nowrap">${_("Login")}</button>
                    </td>
                </tr>
            </table>
            % endif

            % if style=='ajax':
            <table align="center" cellspacing="2px" border="0">
                <tr>
                    <td class="label">${_("User:")}</td>
                    <td><input type="text" id="user" name="user" style="width: 150px;" value="${user}"/></td>
                </tr>
                <tr>
                    <td class="label">${_("Password:")}</td>
                    <td><input type="password" value="${password}" id="password" name="password" style="width: 150px;"/></td>
                </tr>
                <tr>
                    <td>&nbsp;</td>
                    <td align="right">
                        <button type="submit" style="width: 80px; white-space: nowrap">${_("Login")}</button>
                    </td>
                </tr>
            </table> 
            % endif

        </form>
        <div id="message" style="display: none; color: red; text-align: center;">${_("Bad username or password!")}</div>

    </div>
</%def>

