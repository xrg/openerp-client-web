<form xmlns:py="http://purl.org/kid/ns#" method="post" id="${name}" name="${name}" action="${action}" enctype="multipart/form-data">
    <input type="hidden" value="${limit}" name="_terp_limit" id="_terp_limit"/>
    <input type="hidden" value="${offset}" name="_terp_offset" id="_terp_offset"/>
    <span py:for="field in hidden_fields" py:replace="field.display(value_for(field), **params_for(field))"/>
 
    <script type="text/javascript">    
        function toggle_sidebar(element_id, forced) {
        	var sb = $(element_id);
            
            sb.style.display = forced ? forced : (sb.style.display == "none" ? "" : "none");            
            set_cookie("terp_sidebar", sb.style.display);

            var img = getElementsByTagAndClassName('img', null, 'sidebar_hide')[0];
            if (sb.style.display == "none")
                img.src = '/static/images/sidebar_show.gif';
            else
                img.src = '/static/images/sidebar_hide.gif';
        }
    </script>

    <table border="0" cellpadding="0" cellspacing="0" width="100%" py:if="screen">
        <tr>
            <td valign="top" width="100%">
                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr><td valign="top" py:if="search" py:content="search.display(value_for(search), **params_for(search))" width="100%"></td></tr>
                        <tr>
                            <td py:if="search">
                                <div class="spacer"/>
                                <div class="toolbar">
                                    <button type="button" onclick="submit_search_form()">Find</button>
                                </div>
                                <div class="spacer"/>
                            </td>
                        </tr>
                        <tr><td valign="top" width="100%" py:content="screen.display(value_for(screen), **params_for(screen))"></td></tr>
                </table>
            </td>
            <td py:if="screen.hastoolbar and screen.toolbar" width="163" valign="top" style="padding-left: 4px">
		
				<table border="0" cellpadding="0" cellspacing="0" width="160" id="sidebar" style="display:none">
	                <tr py:if="'print' in screen.toolbar">
	                    <td>
				    		<table border="0" cellpadding="0" cellspacing="0" width="100%" class="sidebox">
								<tr>
                                    <td>
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                            <tr>
            									<td width="8" style="background: #ac0000"/>
            									<td width="7" style="background-color: #363636"/>
            									<td style="font: verdana; color:white; font-weight:bold; font-size:12px; background-color: #363636">REPORTS</td>
            									<td width="25" valign="top" style="background: url(/static/images/head_diagonal.png) no-repeat; background-color: #666666"/>
            									<td width="50" style="background-color: #666666"/>
                                            </tr>
                                        </table>
                                    </td>
								</tr>
							
	    						<tr py:for="item in screen.toolbar['print']" data="${str(item)}" onclick="submit_form('action', null, getNodeAttribute(this, 'data'))">
	    						    <td>
									    <a href="#">${item['string']}</a>								    
									</td>
						        </tr>
						    </table>
                        </td>
                    </tr>
					<tr py:if="'action' in screen.toolbar">
                        <td>											
							<table border="0" cellpadding="0" cellspacing="0" width="100%" class="sidebox">
								<tr>
                                    <td>
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                            <tr>
            									<td width="8" style="background: #ac0000"/>
            									<td width="7" style="background-color: #363636"/>
            									<td style="font: verdana; color:white; font-weight:bold; font-size:12px; background-color: #363636">ACTIONS</td>
            									<td width="25" valign="top" style="background: url(/static/images/head_diagonal.png) no-repeat; background-color: #666666"/>
            									<td width="50" style="background-color: #666666"/>
                                            </tr>
                                        </table>
                                    </td>
								</tr>
	    						<tr py:for="item in screen.toolbar['action']" data="${str(item)}" onclick="submit_form('action', null, getNodeAttribute(this, 'data'))">
	    						    <td colspan="5">			    
							    	    <a href="#">${item['string']}</a>										       			   	
	            				    </td>
	        				    </tr>
			    		    </table>
			    		</td>
			    	</tr>
			    </table>	          
		    </td>	  		    
            
            <td id="sidebar_hide" valign="top" py:if="screen.hastoolbar and screen.toolbar">
               <img src="/static/images/sidebar_show.gif" border="0" onclick="toggle_sidebar('sidebar');" style="cursor: pointer;"/>
            </td>
        </tr>
    </table>
</form>
