<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
    <title>Process</title>

    <link type="text/css" rel="stylesheet" href="/static/workflow/css/process_box.css"/>
    <link type="text/css" rel="stylesheet" href="/static/workflow/css/process.css"/>

    <script src='/static/workflow/javascript/draw2d/wz_jsgraphics.js'></script>
    <script src='/static/workflow/javascript/draw2d/mootools.js'></script>
    <script src='/static/workflow/javascript/draw2d/moocanvas.js'></script>
    <script src='/static/workflow/javascript/draw2d/draw2d.js'></script>

    <script src='/static/workflow/javascript/process_box.js'></script>
    <script src='/static/workflow/javascript/process.js'></script>

    <script type="text/javascript">
        MochiKit.DOM.addLoadEvent(function(evt){
            var wkf = new openerp.process.Workflow('process_canvas');

            var id = getElement('id').value;
            var res_model = getElement('res_model').value;
            var res_id = getElement('res_id').value;

            wkf.load(id, res_model, res_id);
    	});
    </script>
</head>

<body>

<table class="view" width="100%" border="0" cellpadding="0" cellspacing="0">
    <tr>
        <td width="100%" valign="top">
            <table width="100%" class="titlebar">
                <tr>
                    <td width="32px" align="center">
                        <img src="/static/images/icon.gif"/>
                    </td>
                    <td width="100%" py:content="title" id="process_title">Title</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <input type="hidden" id="id" value="$id"/>
            <input type="hidden" id="res_model" value="$res_model"/>
            <input type="hidden" id="res_id" value="$res_id"/>
            <div id="process_canvas"></div>
        </td>
    </tr>
</table>

</body>
</html>
