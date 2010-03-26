<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
<title>${_("Workflow")}</title>
 <!--meta content="text/html; charset=ISO-8859-1" http-equiv="content-type"-->
    <title></title>  
	<link type="text/css" rel="stylesheet" href="/openerp/static/workflow/css/graph.css"/>
	
	<script src="/openerp/static/workflow/javascript/draw2d/wz_jsgraphics.js"></script>
    <script src="/openerp/static/workflow/javascript/draw2d/mootools.js"></script>
    <script src="/openerp/static/workflow/javascript/draw2d/moocanvas.js"></script>
    <script src="/openerp/static/workflow/javascript/draw2d/draw2d.js"></script>
    
	<script src="/openerp/static/workflow/javascript/connector.js"></script>
	<script src="/openerp/static/workflow/javascript/conn_anchor.js"></script>
	<script src="/openerp/static/workflow/javascript/conn_decorator.js"></script>
    <script src="/openerp/static/workflow/javascript/workflow.js"></script>
    <script src="/openerp/static/workflow/javascript/toolbar.js"></script>
    <script src="/openerp/static/workflow/javascript/ports.js"></script>
    <script src="/openerp/static/workflow/javascript/state.js"></script>
    <script src="/openerp/static/workflow/javascript/infobox.js"></script>

    <style>
        body, html {
            padding: 5px;
        }
    </style>
    
    <script type="text/javascript">

    	var WORKFLOW;
    	
        MochiKit.DOM.addLoadEvent(function(evt){
    		WORKFLOW = new openobject.workflow.Workflow('canvas');
	        WORKFLOW.setViewPort("viewport");
    	});
        
    </script>
</%def>

<%def name="content()">
    <table class="view" border="0">
        <tr>
            <td colspan="2">
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/openerp/static/images/stock/gtk-refresh.png"/>
                        </td>
                        <td width="100%">${_('Workflow (%s)') % wkf['name']}</td>
                    </tr>
                </table>
                <input type="hidden" id="wkf_id" value="${wkf['id']}"/>
                <input type="hidden" id="_terp_editable" name="_terp_editable" value="False"/>
                <input type="hidden" id="_terp_model" name="_terp_model" value="workflow"/>
                <input type="hidden" id="workitems" name="workitems" value="${workitems}"/>
                <input type="hidden" id="node" name="node" value="workflow.activity"/>
                <input type="hidden" id="connector" name="connector" value="workflow.transition"/>
                <input type="hidden" id="src_node" name="src_node" value="act_from"/>
                <input type="hidden" id="des_node" name="des_node" value="act_to"/>
            </td>
        </tr>
        <tr>
            <td>
                <table width="100%">
                    <tr>
                        ##<td width="36px" valign="top" id="toolbox"></td>
                        <td height="500" width="auto" valign="top">
                            <div id="viewport" style="position: relative; width: 100%; height: 500px; border: 1px solid gray; overflow: auto;">
                                <div id="canvas" style="position: absolute;  width: 3000px; height: 3000px;">
                                    <span id="loading" style="color: red; width:100%;" align="right">${_("Loading...")}</span>
                                </div>
                            </div>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr class="toolbar">
            <td align="right" colspan="2">
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td align="left" id="status" style="width: 100%; ">&nbsp;</td>
                            <td><button type="button" onclick="window.close()">${_("Close")}</button></td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</%def>
