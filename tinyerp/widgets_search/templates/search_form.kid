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
    <input type="hidden" name="_terp_editable" value="${editable}"/>
	<input type="hidden" name="_terp_fields_type" value="${str(fields_type)}"/>
	
	<input type="hidden" value="${limit}" name="_terp_limit" id="_terp_limit"/>
    <input type="hidden" value="${offset}" name="_terp_offset" id="_terp_offset"/>
    		    	
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
	        <td align="left">		        		    		
   				<button type="button" id='find_button' title="Find Records..." onclick="${onfind}">Find</button>
                <button type="button" id='cancel_button' title="Cancel..." onclick="${oncancel}">Cancel</button>
                <button type="button" id='select_button' title="Select Record(s)..." onclick="${onok}">Select</button>
	        </td>
	    </tr>
	</table>
</form>

