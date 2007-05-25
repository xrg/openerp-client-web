<form method="post" action="${action}" id="${name}" name="${name}" xmlns:py="http://purl.org/kid/ns#">
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
	
	<input type="hidden" value="${limit}" name="limit" id="limit"/>
    <input type="hidden" value="${offset}" name="offset" id="offset"/>
    		    	
	<span py:for="field in hidden_fields" py:replace="field.display(value_for(field), **params_for(field))"/>
	
	<table class="fields" width="100%">
	    <tr>
	        <td>
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
	        </td>
	    </tr>
	    <tr>
	        <td>		        		    		
   				<button type="button" id='find_button' title="Find Records..." onclick="${onfind}">Find</button>
                <button type="button" id='cancel_button' title="Cancel..." onclick="${oncancel}">Cancel</button>
                <button type="button" id='ok_button' title="Select Record..." onclick="${onok}">OK</button>
	        </td>
	    </tr>
	</table>
</form>

