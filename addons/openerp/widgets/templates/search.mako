<div id="search_filter_data">
	${display_member(frame)}
	<table id="filter_table" style="display: none;">
		<% x = 0 %>
		% for f,k in enumerate(filter_domain):
			% if len(k) >1:
			    <tr id="filter_row/${x}" class="filter_row_class">
					<td align="right" class="filter_column" id="filter_column/${x}">
						<select id="filter_fields/${x}" class="filter_fields">
							% for field in fields_list:
								<option kind="${field[2]}" value="${field[0]}" ${py.selector(field[0]==k[0])}>${field[1]}</option>
							% endfor
					       </select>
						<select id="expr/${x}" class="expr">
							% for operator, description in operators_map:
								<option value="${operator}" ${py.selector(operator==k[1])}>${description}</option>
							% endfor
						</select>
					       <input type="text" class='qstring' id="qstring/${x}" value="${k[2] or ''}" />
					</td>
					% if len(filter_domain[f -1]) == 1:
					<td class="and_or" id="and_or/${x}">
						<select id="select_andor/${x}" class="and_or">
						% if filter_domain[f -1] == '&':
							<option value="AND">AND</option>
						%else:
							<option value="OR">OR</option>
						% endif
						</select>
					</td>
					% endif
					<td id="image_col/${x}" class="image_col">
						<img id="img_remove" width="18" height="18" src="/openerp/static/images/stock-disabled/gtk-remove.png" onclick="remove_row(this)" style="cursor: pointer;"/>
					</td>
			    </tr>
			    <% x = x+1 %>
			% endif
		% endfor
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
				<a class="button" href="javascript: void(0)" onclick="add_filter_row();">
					<span class="add">Add</span>
				</a>
				
			</li>
		</ul>
	</div>
</div>
