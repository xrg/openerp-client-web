<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Login</title>
</head>

<body>
    <div class="view">
        <br/>

        <div class="box2 welcome">Administration</div>    
        <div class="box2">
            <table align="center" cellspacing="2px" border="0">
                <tr>
                    <td>
                        <button type="button" onclick="location.href='/dbadmin'">Database Management</button>
                    </td>
                    <td>
                        <button type="button" onclick="location.href='/configure'">Configuration Editor</button>
                    </td>
                </tr>
            </table>
        </div>
    
        <div class="box2">
            <table align="center" border="0" width="100%">
                <tr>                            
                    <td align="right">
                        <button type="button" onclick="window.location.href='/login'">Cancel</button>
                    </td>
                </tr>
            </table>
        </div>
    </div>
</body>
</html>