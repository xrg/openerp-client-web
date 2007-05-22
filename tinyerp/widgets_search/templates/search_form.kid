<table class="fields" width="100%" border="0" cellpadding="0" cellspacing="0" xmlns:py="http://purl.org/kid/ns#" >
    <tr>
        <td>
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

			<div class="tabber" id="search_view_notebook">
				<div class="tabbertab">
					<h3>Basic Search</h3>
		    	  	<span py:replace="bframe.display()" py:if="bframe"/>
				</div>
				<div class="tabbertab">
					<h3>Advance Search</h3>
	    			<span py:replace="aframe.display()" py:if="aframe"/>
				</div>
			</div>
            <div class="spacer"></div>
            
	        <input type="hidden" value="${limit}" name="limit" id="limit"/>
	    	<input type="hidden" value="${offset}" name="offset" id="offset"/>

            <div class="toolbar">
				<table>
					<tr>
                        <td>			    		    
	        				<button type="button" id='find_button' title="Find Records..." onclick="${onfind}">Find</button>
				    		<button type="button" id='cancel_button' title="Cancel..." onclick="${oncancel}">Cancel</button>
					    	<button type="button" id='ok_button' title="Select Record..." onclick="${onok}">OK</button>
				    	</td>
    					<td width="100%"></td>
			            <td><button type="button" name="first" onclick="$('offset').value = 0; ${onfind}">First</button></td>
	    		        <td><button type="button" name="prev" onclick="$('offset').value = parseInt($('offset').value) - parseInt($('limit').value); ${onfind}">Prev</button></td>
			            <td style="padding: 0 4px">
	        	            (${offset} to ${limit + offset})
		    	        </td>
		        	    <td><button type="button" name="next" onclick="$('offset').value = parseInt($('offset').value) + parseInt($('limit').value); ${onfind}">Next</button></td>
		        	    <td><button type="button" name="last" onclick="return false">Last</button></td>						
				    </tr>
		    	</table>
		    </div>
		</form>
        </td>
    </tr>
</table>