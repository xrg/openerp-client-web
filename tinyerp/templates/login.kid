<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Login</title>
</head>

<body>
    <div class="view">
        <br/>
        <div class="box2 welcome">
            Welcome to Tiny ERP
        </div>

            <form action="${target}" method="post" name="loginform">
                <input type="hidden" py:for="key, value in origArgs.items()" name="${key}" value="${str(value)}"/>
                <input type="hidden" name="login_action" value="login"/>

                <div class="box2">
                    <table align="center" cellspacing="2px" border="0">
                        <tr>
                            <td class="label">Server :</td>
                            <td py:content="url"/>
                        </tr>
                        <tr>
                            <td class="label">Database :</td>
                            <td>
                                <select name="db" style="width: 302px;">
                                    <span py:if="dblist and (dblist is not -1)">
                                        <option py:for="v in dblist or []" py:content="v" selected="${tg.selector(v==db)}">dbname</option>
                                    </span>
                                </select>
                            </td>
                        </tr>

                        <tr>
                            <td class="label">User :</td>
                            <td><input type="text" id="user" name="user" style="width: 300px;" value="${user}"/></td>
                        </tr>
                        <tr>
                            <td class="label">Password :</td>
                            <td><input type="password" value="${passwd}" id="passwd" name="passwd" style="width: 300px;"/></td>
                        </tr>
                        <tr>
                            <td></td>
                            <td align="right">
                                <button type="button" style="width: 80px; white-space: nowrap; margin-right: 4px;" onclick="location.href='/dbadmin'">Manage</button>
                                <button type="submit" style="width: 80px; white-space: nowrap">Login</button>
                            </td>
                        </tr>
                    </table>
                </div>
            </form>

        <div class="box2 message" id="message" py:if="message" py:content="message"/>

        <br/>
        <center>
            <img src="/static/images/developped_by.png" border="0" width="200" height="60" alt="${_('Developped by Axelor and Tiny')}" usemap="#devby_map"/>
            <map name="devby_map">
                <area shape="rect" coords="0,20,100,60" href="http://axelor.com" target="_blank"/>
                <area shape="rect" coords="120,20,200,60" href="http://tinyerp.com" target="_blank"/>
            </map>
        </center>
    </div>
</body>

</html>

