<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>View Editor</title>
</head>
<body>
    <table class="view" border="1">
        <tr>
            <th width="300">${model}</th>
            <th align="left">TODO: [add] [delete] [edit]</th>
        </tr>
        <tr>
            <td id="view_tree" height="500">
                <div py:content="tree.display()" style="overflow: scroll; width: 100%; height: 100%; border: solid #999999 1px;"/>
            </td>
            <td id="view_prop">
                TODO: Property Editor
            </td>
        </tr>
        <tr class="toolbar">
            <td colspan="2" align="right">TODO: [save] [cancel]</td>
        </tr>
    </table>
</body>
</html>
