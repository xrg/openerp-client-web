<table>
	<tr>
		<td>
			% if def_checked:
			<div id="active_filter" class="active_filter" onclick="search_filter(getElement('${filter_id}'), this);" title="${help}">
				% if icon:
					<div align="center">
						<img src="${icon}" width="16" height="16"/>
					</div>	
				% endif
				% if help !=text_val:
					<div>
						${text_val}
					</div>
				% endif
				<input ${py.attrs(attrs)} style="display:none;"
					type="checkbox"
					id="${filter_id}"
					name="${filter_id}"
					class="checkbox grid-domain-selector" 
					onclick="search_filter(this);" 
					value="${filter_domain}"
					group_by_ctx="${group_context}"
					checked
					title="${help}">
				</input>
			</div>			
		% else:
			<div id="inactive_filter" class="inactive_filter" onclick="search_filter(getElement('${filter_id}'), this);" title="${help}">
				% if icon:
					<div align="center">
						<img src="${icon}" width="16" height="16"/>
					</div>	
				% endif
				% if help !=text_val:
					<div>
						${text_val}
					</div>
				% endif
				<input ${py.attrs(attrs)} style="display:none;"
					type="checkbox"
					id="${filter_id}"
					name="${filter_id}"
					class="checkbox grid-domain-selector" 
					onclick="search_filter(this);" 
					value="${filter_domain}"
					group_by_ctx="${group_context}"
					title="${help}">
				</input>
			</div>
		% endif
		</td>
	</tr>
</table>
