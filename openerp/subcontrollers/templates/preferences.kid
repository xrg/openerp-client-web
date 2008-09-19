<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>${screen.string}</title>
</head>
<body>
    <div class="view">
        <form action="/pref/ok" method="post">
            <table align="center">
                <tr>
                    <td class="toolbar welcome">${screen.string}</td>
                </tr>
                <tr>
                    <td py:content="screen.display()"></td>
                </tr>
                <td class="toolbar" align="right">
                    <button type='button' style="width: 80px" onclick="history.back()">Cancel</button>
                    <button type='submit' style="width: 80px">OK</button>
                </td>
            </table>
        </form>
    </div>
</body>
</html>
