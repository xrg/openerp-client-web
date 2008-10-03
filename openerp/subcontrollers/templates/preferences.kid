<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>${params.string}</title>
</head>
<body>
    <div class="view">
        <form action="/pref/ok" method="post">
            <table align="center">
                <tr>
                    <td class="toolbar welcome">${params.string}</td>
                </tr>
                <tr>
                    <td py:content="form.display()"></td>
                </tr>
                <td class="toolbar" align="right">
                    <button type='button' style="width: 80px" onclick="window.location.href='/'">Cancel</button>
                    <button type='submit' style="width: 80px">Save</button>
                </td>
            </table>
        </form>
    </div>
</body>
</html>
