<form xmlns:py="http://purl.org/kid/ns#" method="post" id="${name}" name="${name}" action="${action}" enctype="multipart/form-data">
    <span py:for="field in hidden_fields" py:replace="field.display(value_for(field), **params_for(field))"/>
 
    <script type="text/javascript">
    
    function toggle_sidebar(element_id) {
    	var element = document.getElementById(element_id);
        
    	if (element !== null) {
	  		if (element.style.display == "none") {
	    	    element.style.display = "block";  	    	    
	    	    set_cookie(element_id, "block");	    	    
		    } else {
    		    element.style.display = "none";    
    		    set_cookie(element_id, "none");
		    }
       	}
    }    
        
    </script>
    <table border="0" cellpadding="0" cellspacing="0" width="100%" py:if="screen">
        <tr>
            <td valign="top" py:content="screen.display(value_for(screen), **params_for(screen))" width="100%"></td>
            <td py:if="screen.hastoolbar and screen.toolbar" width="163" valign="top" style="padding-left: 4px">
                <div id="toolbar_hide">
					<a href="#" onclick="toggle_sidebar('sidebar');">
						<img src="/static/images/toolbar_hide.png" alt="|" border="0"/>
					</a>
				</div>				
		
				<div id="sidebar" style="display:none">
    				<table border="0" cellpadding="0" cellspacing="0" width="160">
		                <tr>
		                    <td>
					    		<table border="0" cellpadding="0" cellspacing="0" width="100%" py:if="'print' in screen.toolbar">
									<tr>
										<td width="8" bgcolor="#ac0000"></td>
										<td width="7" bgcolor="#363636"></td>
										<td bgcolor="#363636" style="font:verdana; color:white; font-weight:bold; font-size:12px">
											REPORTS
										</td>
										<td width="25" bgcolor="#666666" valign="top">
											<img src="/static/images/head_diagonal.png"/>
										</td>
										<td bgcolor="#666666">
											&nbsp;
											&nbsp;
											&nbsp;
										</td>
									</tr>
								</table>
								
								<div class="toolbar_button" py:if="'print' in screen.toolbar">
								    <table border="0" cellpadding="0" cellspacing="0" width="100%">
			    						<tr py:for="item in screen.toolbar['print']" data="${str(item)}" onclick="submit_form('action', null, getNodeAttribute(this, 'data'))">
			    						    <td>
											    <a href="#" class="toolbar_button">${item['string']}</a>								    
											</td>
								        </tr>
								    </table>
								</div>				
									
								<table border="0" cellpadding="0" cellspacing="0" width="100%" py:if="'action' in screen.toolbar">
									<tr>
										<td width="8" bgcolor="#ac0000"></td>
										<td width="7" bgcolor="#363636"></td>
										<td bgcolor="#363636" style="font:verdana; color:white; font-weight:bold; font-size:12px">
											ACTIONS
										</td>
										<td width="25" bgcolor="#666666" valign="top">
											<img src="/static/images/head_diagonal.png"/>
										</td>
										<td bgcolor="#666666">
										&nbsp;
										&nbsp;
										&nbsp;
										</td>
									</tr>
				    			</table>
				    			
					    		<div class="toolbar_button" py:if="'action' in screen.toolbar">	
					    		    <table border="0" cellpadding="0" cellspacing="0" width="100%">
			    						<tr py:for="item in screen.toolbar['action']" data="${str(item)}" onclick="submit_form('action', null, getNodeAttribute(this, 'data'))">
			    						    <td>			    
									    	    <a href="#" class="toolbar_button">${item['string']}</a>										       			   	
			            				    </td>
			        				    </tr>
					    		    </table>
				    			</div>
				    		</td>
				    	</tr>
				    </table>
                </div>		           		    		          
		    </td>	  		    
        </tr>
    </table>
</form>
