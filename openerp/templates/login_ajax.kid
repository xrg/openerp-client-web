<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
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

</head>

<body>
    <div class="view">

        <form onsubmit="return do_login()" action="/" method="post" name="loginform">
            <input type="hidden" id="location" name="location" value="$location"/>
            <input type="hidden" id="db" name="db" value="$db"/>

            <table align="center" border="0" py:if="style=='ajax_small'">
                <tr>
                    <td><strong>User:</strong></td>
                </tr>
                <tr>
                    <td><input type="text" id="user" name="user" style="width: 150px;" value="${user}"/></td>
                </tr>
                <tr>
                    <td><strong>Password:</strong></td>
                </tr>
                <tr>
                    <td><input type="password" value="${password}" id="password" name="password" style="width: 150px;"/></td>
                </tr>
                <tr>
                    <td>
                        <button type="submit" style="width: 80px; white-space: nowrap">Login</button>
                    </td>
                </tr>
            </table> 

            <table align="center" cellspacing="2px" border="0" py:if="style=='ajax'">
                <tr>
                    <td class="label">User:</td>
                    <td><input type="text" id="user" name="user" style="width: 150px;" value="${user}"/></td>
                </tr>
                <tr>
                    <td class="label">Password:</td>
                    <td><input type="password" value="${password}" id="password" name="password" style="width: 150px;"/></td>
                </tr>
                <tr>
                    <td>&nbsp;</td>
                    <td align="right">
                        <button type="submit" style="width: 80px; white-space: nowrap">Login</button>
                    </td>
                </tr>
            </table> 

        </form>
        <div id="message" style="display: none; color: red; text-align: center;">Bad username or password!</div>

    </div>
</body>

</html>

