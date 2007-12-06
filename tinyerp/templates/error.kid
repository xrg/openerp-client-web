<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <link href="/static/css/style.css" rel="stylesheet" type="text/css" />
    <title>${title}</title>
 </head>

<body>

    <div class="view">
        <table border="0" cellpadding="0" cellspacing="0" align="center">
            <tr>
                <td height="15px"/>
            </tr>
            <tr>
                <td class="errorbox welcome">
                    ${title}
                </td>
            </tr>
            <tr>
                <td height="5px"/>
            </tr>
            <tr>
                <td class="errorbox" style="padding: 30px;">
                    <pre py:content="message"/>
                </td>
            </tr>
            <tr>
                <td height="5px"/>
            </tr>
            <tr>
                <td class="errorbox" align="right">
                    <button type="button" onclick="history.length > 1 ? history.back() : window.close()">OK</button>
                </td>
            </tr>
        </table>
    </div>


</body>

</html>
