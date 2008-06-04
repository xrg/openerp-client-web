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
    	
    	
    	var workflow;
    	var state;
    	var conn;
    	
    	var tr_info;
    	var loading;
    	
    	function initLoad()
    	{
    		loading = document.getElementById('loading');
    		
    		
    		state = new openerp.workflow.State();
	        state.setDimension(100, 60);
			state.setBackgroundColor(new draw2d.Color(255, 255, 255));
	        workflow.addFigure(state, 100, 20);
			state.initPort();
			var html_state = state.getHTMLElement();	
			html_state.style.display = 'none';
			
			var state_ports = state.getPorts();
			
			conn = new openerp.workflow.Connector(999);
			conn.setSource(state_ports.get(0));
			conn.setTarget(state_ports.get(3));			
			workflow.addFigure(conn);
			
			var html_conn = conn.getHTMLElement();
			html_conn.style.display = 'none';
			
			tr_info = document.getElementById('tr_info');
			draw(document.getElementById('wkf_combo'));
			
    	}
    	
	    function draw(val)
	    {
	    	loading.style.display = '';
	    	workflow.draw_graph(val.value);
	    }	    
	    
		function create_activity(id) {
			//log(id);
			workflow.create_state(id);
		}	
			
		function create_transition(id) {
			workflow.update_conn(id);	
		}
    </script>
</head>



<body onload="javascript: initLoad();">
	<table class="view" style="height: 100%;">
		<tr>
			<td width='100%' valign="top">
				<table width="100%" cellspacing="0" cellpadding="0" border="0">
					<tr>
						<td>								
							<table class="titlebar" width="100%">									
									<tr>
										<td width="32" align="center">
											<img src="/static/images/icon.gif"/>
										</td>
										<td width="100%">Workflow Editor</td>											
										<td width="16" valign="middle" align="center">
											<img class="button" width="16" height="16" border="0" src="/static/images/stock/gtk-help.png"/>
										</td>
									</tr>
							</table>								
						</td>
					</tr>
					<tr>
						 <td>
			                <div class="toolbar">
			                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
			                        <tr>
			                        	<td align="left" width='100%'>
			                        		<span>Workflow  :</span>
									 		<select id="wkf_combo" onchange = "javascript:draw(this);">
									 			<option py:for = "item in data" value="${item['id']}">${item['name']}</option>						 			
									 		</select>
									 	</td>	
									 	<td align="right" id="tr_info" style="visibility:hidden;"></td>					 
					 				</tr>	
			                    </table>
			                </div>
			            </td>
					</tr>
							
					<tr>
						<td>
							<table border="0" cellpadding="0" cellspacing="0" width="100%">
								<tr>
									<td>
									    <div id="viewport" style="position: relative; width: 100%; height: 380px; border: 1px solid; overflow: auto;">
									        <div id="canvas" style="position: absolute;  width: 3000px; height: 3000px;">
									        <span id="loading" style="color: red; width:100%;" align="right">Loading...</span>
									        </div>
									    </div>
									</td>
								</tr>
							</table>
					    </td>
					 </tr>
				</table>
			</td>
		</tr>
	</table>
    <script type="text/javascript">

        workflow = new openerp.workflow.Workflow('canvas');
        workflow.setViewPort("viewport");
        workflow.setBackgroundImage(null, false);

        var toolbar = new openerp.workflow.Toolbar();
        workflow.setToolWindow(toolbar, 30, 30);
    </script>

</body>
</html>
