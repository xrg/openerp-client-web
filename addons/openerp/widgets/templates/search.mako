<div id="search_filter_data">
	${display_member(frame)}
	<table id="filter_table" style="display: none;">
	    <tr id="filter_row" class="filter_row_class">
	    	<td align="right" class="filter_column" id="filter_column">
	    		<select id="filter_fields" class="filter_fields">
	    			% for field in fields_list:
	                	<option kind="${field[2]}" value="${field[0]}">${field[1]}</option>
	                % endfor
	            </select>
	    		<select id="expr" class="expr">
	    			% for operator, description in operators_map:
	                	<option value="${operator}">${description}</option>
	                % endfor
	            </select>
	            <input type="text" class='qstring' id="qstring"/>
	    	</td>
	    	
	    	<td class="and_or" id="and_or"></td>
	    	
	    	<td id="image_col">
	    		<img id="img_remove" width="18" height="18" src="/openerp/static/images/stock-disabled/gtk-remove.png" onclick="remove_row(this)" style="cursor: pointer;"/>
	    	</td>
	    </tr>
	</table>
	<div class="custom-filter">
		<ul>
			<li>
				<select name="filter_list" id="filter_list" onchange="search_filter();">
	                % for f in filters_list:
	                <option value="${f[0]}">${f[1]}</option>
	                % endfor
	            </select>
			</li>
			<li>
				<a class="button">
					<span class="add" onclick="add_filter_row();">Add</span>
				</a>
				
			</li>
		</ul>
	</div>
</div>
