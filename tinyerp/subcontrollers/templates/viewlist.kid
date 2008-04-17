<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>Manage Views ($model)</title>
    <script type="text/javascript">
        function do_select(id, src){
            var radio = MochiKit.DOM.getElement(src + '/' + id);
            radio.checked = true;
        }
    </script>
</head>
<body>

    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/static/images/icon.gif"/>
                        </td>
                        <td width="100%">Manage Views ($model)</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td py:content="screen.display()">List View</td>
        </tr>
        <tr>
            <td>
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td>
                                <button type="button" onclick="alert('Not implemented yet!')">New</button>
                                <button type="button" onclick="alert('Not implemented yet!')">Edit</button>
                                <button type="button" onclick="alert('Not implemented yet!')">Remove</button>
                            </td>
                            <td width="100%"></td>
                            <td>
                                <button type="button" onclick="window.close()">Close</button>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>

</body>
</html>
