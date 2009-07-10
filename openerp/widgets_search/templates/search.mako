${display_member(frame)}
<table id="filter_table" style="display: none;">
    <tr id="filter_row" class="filter_row_class">
    	<td align="right" id="filter_column">
    		<select name="fields" id="fields">
    			% for field in fields_list:
                	<option value="${field[0]}">${field[1]}</option>
                % endfor
            </select>
    		<select name="domain_text" id="domain_text">
    			% for val in middle_string:
                	<option value="${val[0]}">${val[1]}</option>
                % endfor
            </select>
            <input type="text" name="qstring" id="qstring"/>
    	</td>
    	
    	<td class="and_or"></td>
    	
    	<td id="image_col">
    		<img id="img_remove" width="18" height="18" src="/static/images/stock-disabled/gtk-remove.png" onclick="remove_row(this)" style="cursor: pointer;"/>
    	</td>
    </tr>
</table>

<table>
    <tr>
    	<td align="right">
    		<select name="filter_list" id="filter_list">
                % for f in filters_list:
                <option value="${f[0]}">${f[1]}</option>
                % endfor
            </select>            
    	</td>
    	<td>
    		<img width="18" height="18" src="/static/images/stock-disabled/gtk-add.png" onclick="add_filter_row();" style="cursor: pointer;"/>
    	</td>
    </tr>
</table>

