<table>
	<tr>
		<td class=label>
			${text_val}:
		</td>
		<td>
			% if def_checked:
			<input ${py.attrs(attrs)} 
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
			% else:
			<input ${py.attrs(attrs)} 
					type="checkbox"
					id="${filter_id}"
					name="${filter_id}"
					class="checkbox grid-domain-selector" 
					onclick="search_filter(this);" 
					value="${filter_domain}"
					group_by_ctx="${group_context}"
					title="${help}">
			</input>
			% endif
		</td>
	</tr>
</table>
