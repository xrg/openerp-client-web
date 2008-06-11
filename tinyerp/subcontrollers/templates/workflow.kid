<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Graph</title>
 <!--meta content="text/html; charset=ISO-8859-1" http-equiv="content-type"-->
    <title></title>  
	<link type="text/css" rel="stylesheet" href="/static/workflow/css/graph.css"/>
	
	<script src='/static/workflow/javascript/draw2d/wz_jsgraphics.js'></script>
    <script src='/static/workflow/javascript/draw2d/mootools.js'></script>
    <script src='/static/workflow/javascript/draw2d/moocanvas.js'></script>
    <script src='/static/workflow/javascript/draw2d/draw2d.js'></script>
    
	<script src='/static/workflow/javascript/connector.js'></script>
	<script src='/static/workflow/javascript/conn_anchor.js'></script>
    <script src='/static/workflow/javascript/workflow.js'></script>
    <script src='/static/workflow/javascript/toolbar.js'></script>
    <script src='/static/workflow/javascript/ports.js'></script>
    <script src='/static/workflow/javascript/state.js'></script>
    <script src='/static/workflow/javascript/infobox.js'></script>

    <style>
        body, html {
            padding: 5px;
        }
    </style>
    
    <script type="text/javascript">

    	var WORKFLOW;
    	
        MochiKit.DOM.addLoadEvent(function(evt){
    		WORKFLOW = new openerp.workflow.Workflow('canvas');
	        WORKFLOW.setViewPort("viewport");
    	});
        
    </script>
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
                        <td width="100%" py:content="_('Workflow (%s)' % wkf['name'])">Workflow</td>
                    </tr>
                </table>
                <input type="hidden" id="wkf_id" value="${wkf['id']}"/>
            </td>
        </tr>
        <tr>
            <td width="36px" valign="top" id="toolbox"></td>
            <td height="500" width="auto" valign="top">
                <div id="viewport" style="position: relative; width: 100%; height: 500px; border: 1px solid gray; overflow: auto;">
                    <div id="canvas" style="position: absolute;  width: 3000px; height: 3000px;">
                        <span id="loading" style="color: red; width:100%;" align="right">Loading...</span>
                    </div>
                </div>
            </td>
        </tr>
        <tr class="toolbar">
            <td align="right" colspan="2">
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td id="status" width="100%">&nbsp;</td>
                            <td><button type="button" onclick="window.close()">Close</button></td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</body>
</html>
