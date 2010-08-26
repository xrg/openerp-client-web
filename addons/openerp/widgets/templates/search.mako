<div id="search_filter_data">
	% if frame:
		${display_member(frame)}
	% endif
	
	<table>
        <tr>
           <td style="padding:4px; white-space:nowrap;">
                <div id="filters" class="group-expand"><h2><span>Filters</span></h2></div>
                <table id="filter_option_table" style="display:none;">
	                <tbody id="filter_table" style="display:none;">					
					    <tr class="filter_row_class">
		                    <td colspan="1" class="image_col" width="25%">
		                        <button onclick="remove_filter_row(this); return false;">
		                            <img alt="Remove filter row" src="/openerp/static/images/button-b-icons-remove.gif"/>
		                        </button>
		                    </td>
		                    <td colspan="1" class="filterlabel">
                                <label id="filterlabel" value="" class="filterlabel"></label>
                            </td>
                            <td colspan="1">
                                <select class="expr">
                                    % for operator, description in operators_map:
                                        <option value="${operator}" >${description}</option>
                                    % endfor
                                </select>
                            </td>
                            <td colspan="2" align="right" class="filter_column">
                                <input type="text" class='qstring' value="" />
                            </td>
					    </tr>
					</tbody>
					<tbody class="actions">
						<tr class="actions">
	                        <td colspan="2">
	                            <label for="add_filter_and">And</label>
	                            <select class="filter_fields_and" onchange="add_filter_row(this); return jQuery('select.filter_fields_and').val('');">
	                               <option></option>
	                               % for field in fields_list:
	                                   <option kind="${field[2]}" value="${field[0]}">${field[1]}</option>
	                               % endfor
	                            </select>
	                        </td>                       
	                        <td class="filter_column" colspan="2" style="text-align:right; white-space:nowrap;">
	                            <label for="add_filter_or">OR</label>
	                            <select id="filter_fields_or" disabled="disabled" class="filter_fields_or" onchange="addOrBlock(this); return jQuery('select.filter_fields_or').val('');">
	                                <option></option>
	                                % for field in fields_list:
	                                    <option kind="${field[2]}" value="${field[0]}">${field[1]}</option>
	                                % endfor
	                            </select>
	                        </td>
	                    </tr>
	                </tbody>
				</table>
		   </td>
	    </tr>
    </table>
    <script type="text/javascript">
		jQuery('#filters').click(function() {
		    jQuery(this).toggleClass('group-expand group-collapse');
		    jQuery('#filter_option_table').toggle();		    
		});
		
		jQuery(document).ready(function () {
		    
            switch_searchView("${flt_domain | n}");
		});
    </script>	
</div>
