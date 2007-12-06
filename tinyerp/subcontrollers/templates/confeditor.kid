<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Config Editor</title>

    <script type="text/javascript">
        function changepwd(id) {
            if($(id).style.display == 'none') {
                $(id).style.display = '';
            }
            else {
                $(id).style.display = 'none';
            }
        }

    </script>

</head>

<body>
    <div class="view">
    <div class="box2 welcome">Config Editor</div>
        <div py:if="not tg.errors and not passwd or message">
            <form name="config" action="/configure/connect" method="post">
                <div class="box2" id="passwd">
                    <table align="center" border="0" width="100%">
                        <tr>
                            <td align="right" class="label">
                                Password :
                            </td>
                            <td>
                                <input type="password" name="passwd" style="width: 99%;"/>
                            </td>
                        </tr>
                    </table>
                </div>
                <div class="box2">
                    <table align="center" border="0" width="100%">
                        <tr>
                            <td></td>
                            <td align="right">
                                <button type="button" onclick="window.location.href='/login'">Cancel</button>
                                <button type="submit">OK</button>
                            </td>
                        </tr>
                    </table>
                </div>
            </form>
            <div class="box message" id="message" py:if="message" py:content="message"/>
        </div>

        <div py:if="tg.errors or passwd and not message">
            <form name="config" action="/configure/setconf" method="post">
                <div class="box2" id="config">
                    <table align="center" border="0" width="100%">
                        <tr>
                            <td align="right" class="label">
                                Host :
                            </td>
                            <td>
                                <input type="text" name="host" value="${host}" style="width: 99%;"/>
                                <span py:if="'host' in tg.errors">${tg.errors['host']}</span>
                            </td>
                        </tr>
                        <tr>
                            <td align='right' class="label">
                                Port :
                            </td>
                            <td>
                                <input type="text" name="port" value="${port}" style="width: 99%;"/>
                                <span py:if="'port' in tg.errors">${tg.errors['port']}</span>
                            </td>
                        </tr>
                        <tr>
                            <td align='right' class="label">
                                Protocol :
                            </td>
                            <td>
                                <input type="text" name="protocol" value="${protocol}" style="width: 99%;"/>
                                <span py:if="'protocol' in tg.errors">${tg.errors['protocol']}</span>
                            </td>
                        </tr>
                    </table>
                </div>

                <div class="box2" id="changepwd" style="display: ${(not (tg.errors and ('oldpwd' in tg.errors or 'newpwd' in tg.errors or 'repwd' in tg.errors)) or None) and 'none'}">
                    <table align="center" border="0" width="100%">
                        <tr>
                            <td align="right" class="label">
                                Old Password :
                            </td>
                            <td>
                                <input type="password" name="oldpwd" style="width: 99%;"/>
                                <span py:if="'oldpwd' in tg.errors">Password is Incorrect</span>
                            </td>
                        </tr>
                        <tr>
                            <td align='right' class="label">
                                New Password :
                            </td>
                            <td>
                                <input type="password" name="newpwd" style="width: 99%;"/>
                                <span py:if="'newpwd' in tg.errors">Please Enter New Password</span>
                            </td>
                        </tr>
                        <tr>
                            <td align='right' class="label">
                                Retype Password :
                            </td>
                            <td>
                                <input type="password" name="repwd" style="width: 99%;"/>
                                <span py:if="'repwd' in tg.errors">Passwords do not Match</span>
                            </td>
                        </tr>
                    </table>
                </div>

                <div class="box2">
                    <table align="center" border="0" width="100%">
                        <tr>
                            <td>
                                <button type="button" onclick="changepwd('changepwd');">Change Password</button>
                            </td>
                            <td align="right">
                                <button type="button" onclick="window.location.href='/login'">Cancel</button>
                                <button type="submit">OK</button>
                            </td>
                        </tr>
                    </table>
                </div>
            </form>
        </div>
    </div>

</body>
</html>
