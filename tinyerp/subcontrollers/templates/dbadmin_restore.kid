<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Restore Database</title>
 </head>

<body>
    <div class="view">
        <div class="box2 welcome">Restore Database</div>
        <form action="/dbadmin/restore" method="post" enctype="multipart/form-data">
            <div align="center" class="box2">
                <table align="center" width="100%">
                    <tr>
                        <td align="right" class="label" nowrap="nowrap">File :</td>
                        <td class="item" width="100%"><input type="file" name="path" id="path"/></td>
                    </tr>
                    <tr>
                        <td align="right" class="label" nowrap="nowrap">Password :</td>
                        <td class="item" width="100%"><input type="password" name="passwd" id="passwd" style="width: 99%;" /></td>
                    </tr>
                    <tr>
                        <td align="right" class="label" nowrap="nowrap">New Database name :</td>
                        <td class="item" width="100%"><input type="text" name="new_db"  style="width: 99%;" /></td>
                    </tr>
                </table>
            </div>
            <div align="right" class="box2">
                <button type="button" onclick="window.location.href='/dbadmin'">Cancel</button>
                <button type="submit">OK</button>
            </div>

        </form>
        <div class="box2 message" id="message" py:if="message">
            <pre py:content="message"/>
        </div>
    </div>
</body>
</html>
