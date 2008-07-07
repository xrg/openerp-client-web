<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>View Editor</title>
    <script type="text/javascript" src="/static/javascript/form.js"></script>
    <script type="text/javascript" src="/static/javascript/m2o.js"></script>
    <script type="text/javascript" src="/static/javascript/viewed.js"></script>    
</head>
<body>
    <table class="view" border="0">
        <tr>
            <td colspan="2">
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/static/images/icon.gif"/>
                        </td>
                        <td width="100%">View Editor ($view_id - $model)</td>
                    </tr>
                </table>
                <input type="hidden" id="view_model" value="$model"/>
                <input type="hidden" id="view_id" value="$view_id"/>
                <input type="hidden" id="view_type" value="$view_type"/>
            </td>
        </tr>
        <tr>
            <td id="view_tr" height="500" width="auto">
                <div py:content="tree.display()" style="overflow-x: auto; overflow-y: scroll; width: 100%; height: 100%; border: solid #999999 1px;"/>
            </td>
            <td id="view_ed" valign="top"  height="500" width="350"></td>
        </tr>
        <tr class="toolbar">
            <td align="right" colspan="2">
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td><button type="button" title="${_('Create a new inherited view')}" onclick="onInherit('${model}')">Inherited View</button></td>
                            <td width="100%">&nbsp;</td>
                            <td><button type="button" onclick="onPreview()">Preview</button></td>
                            <td><button type="button" onclick="onClose()">Close</button></td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</body>
</html>
