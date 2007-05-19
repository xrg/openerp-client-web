<table class="fields" width="100%" border="0" cellpadding="0" cellspacing="0" xmlns:py="http://purl.org/kid/ns#" >
    <tr>
        <td>
			<div class="tabber" id="search_view_notebook">
				<div class="tabbertab">
					<h3>Basic Search</h3>
					<form method="post" action="${action}" id="${name}" name="${name}">
					    <input type="hidden" name="_terp_model" value="${model}"/>
				    	<input type="hidden" name="_terp_state" value="${state}"/>
					    <input type="hidden" name="_terp_id" value="${str(id)}"/>
					    <input type="hidden" name="_terp_ids" value="${str(ids)}"/>
					    <input type="hidden" name="_terp_view_ids" value="${str(view_ids)}"/>
				    	<input type="hidden" name="_terp_view_mode" value="${str(view_mode)}"/>
					    <input type="hidden" name="_terp_view_mode2" value="${str(view_mode2)}"/>
					    <input type="hidden" name="_terp_domain" value="${str(domain)}"/>
					    <input type="hidden" name="_terp_context" value="${str(context)}"/>
					    <input type="hidden" name="_terp_fields_type" value="${str(fields_type)}"/>
					    <div py:for="field in hidden_fields" py:replace="field.display(value_for(field), **params_for(field))"/>
			    	  	<span py:replace="bframe.display()" py:if="bframe"/>
			    	  	<div class="spacer"></div>
					    <div class="toolbar">
							<table>
								<tr width = "100%">
								    <td>
								        <table border="0" cellpadding="0" cellspacing="0" id="limiter" style="display: none">
									        <tr>
									        	<td class="label">Limit:</td>
										        <td>
										            <input type="text" value="${limit}" name="limit" id="limit" style="width:50px; text-align: center;" />
												</td>
								    			<td class="label">Offset:</td>
										        <td>
						    				    	<input type="text" value="${offset}" name="offset" id="offset" algin ='left' style="width:50px; text-align: center;" />
												</td>
												<td style="padding: 0 4px">
												    <script type="text/javascript">
												        function on_change_limit(){
										    	        var l = $('limit');
										        	    var o = $('offset');
										            	var a = $('pager_text');
											            a.innerHTML = '(' + parseInt(o.value) + ' to ' + (parseInt(o.value) + parseInt(l.value)) + ')';
											            return false;
												        }
												    </script>
												    <button onclick="on_change_limit(); ${onfind}">Change</button>
												</td>
									        </tr>
		    					        </table>
									    <table border="0" cellpadding="0" cellspacing="0" id="pager">
									        <tr>
							    		        <td><button type="button" name="prev" onclick="$('offset').value = parseInt($('offset').value) - parseInt($('limit').value); ${onfind}">Prev</button></td>
									            <td style="padding: 0 4px">
									                <a href="#" onclick="showElement('limiter'); hideElement('pager');" id="pager_text">
								        	            (${offset} to ${limit + offset})
						    			            </a>
								    	        </td>
								        	    <td><button type="button" name="next" onclick="$('offset').value = parseInt($('offset').value) + parseInt($('limit').value); ${onfind}">Next</button></td>
									        </tr>
									    </table>
									</td>
									<td width="100%"></td>
						    		<td>
				        				<button type="button" id='find_button' title="Find Records..." onclick="${onfind}">Find</button>
									</td>
									<td>
							    		<button type="button" id='cancel_button' title="Cancel..." onclick="${oncancel}">Cancel</button>
		    						</td>
						        	<td>
								    	<button type="button" id='ok_button' title="Select Record..." onclick="${onok}">OK</button>
							    	</td>
							    </tr>
					    	</table>
					    </div>
					</form>
				</div>
				<div class="tabbertab">
					<h3>Advance Search</h3>
					<form method="post" action="${action}" id="${name}" name="${name}">
					    <input type="hidden" name="_terp_model" value="${model}"/>
					    <input type="hidden" name="_terp_state" value="${state}"/>
					    <input type="hidden" name="_terp_id" value="${str(id)}"/>
				    	<input type="hidden" name="_terp_ids" value="${str(ids)}"/>
					    <input type="hidden" name="_terp_view_ids" value="${str(view_ids)}"/>
					    <input type="hidden" name="_terp_view_mode" value="${str(view_mode)}"/>
					    <input type="hidden" name="_terp_view_mode2" value="${str(view_mode2)}"/>
				    	<input type="hidden" name="_terp_domain" value="${str(domain)}"/>
					    <input type="hidden" name="_terp_context" value="${str(context)}"/>
					    <input type="hidden" name="_terp_fields_type" value="${str(fields_type)}"/>
					    <div py:for="field in hidden_fields" py:replace="field.display(value_for(field), **params_for(field))"/>
		    			<span py:replace="aframe.display()" py:if="aframe"/>
		    				<div class="spacer"></div>
					    <div class="toolbar">
							<table>
								<tr width = "100%">
								    <td>
								        <table border="0" cellpadding="0" cellspacing="0" id="limiter" style="display: none">
									        <tr>
									        	<td class="label">Limit:</td>
										        <td>
										            <input type="text" value="${limit}" name="limit" id="limit" style="width:50px; text-align: center;" />
												</td>
								    			<td class="label">Offset:</td>
										        <td>
						    				    	<input type="text" value="${offset}" name="offset" id="offset" algin ='left' style="width:50px; text-align: center;" />
												</td>
												<td style="padding: 0 4px">
												    <script type="text/javascript">
												        function on_change_limit(){
										    	        var l = $('limit');
										        	    var o = $('offset');
										            	var a = $('pager_text');
											            a.innerHTML = '(' + parseInt(o.value) + ' to ' + (parseInt(o.value) + parseInt(l.value)) + ')';
											            return false;
												        }
												    </script>
												    <button onclick="on_change_limit(); ${onfind}">Change</button>
												</td>
									        </tr>
		    					        </table>
									    <table border="0" cellpadding="0" cellspacing="0" id="pager">
									        <tr>
							    		        <td><button type="button" name="prev" onclick="$('offset').value = parseInt($('offset').value) - parseInt($('limit').value); ${onfind}">Prev</button></td>
									            <td style="padding: 0 4px">
									                <a href="#" onclick="showElement('limiter'); hideElement('pager');" id="pager_text">
								        	            (${offset} to ${limit + offset})
						    			            </a>
								    	        </td>
								        	    <td><button type="button" name="next" onclick="$('offset').value = parseInt($('offset').value) + parseInt($('limit').value); ${onfind}">Next</button></td>
									        </tr>
									    </table>
									</td>
									<td width="100%"></td>
						    		<td>
				        				<button type="button" id='find_button' title="Find Records..." onclick="${onfind}">Find</button>
									</td>
									<td>
							    		<button type="button" id='cancel_button' title="Cancel..." onclick="${oncancel}">Cancel</button>
		    						</td>
						        	<td>
								    	<button type="button" id='ok_button' title="Select Record..." onclick="${onok}">OK</button>
							    	</td>
							    </tr>
					    	</table>
					    </div>
					</form>
				</div>
			</div>
        </td>
    </tr>
</table>