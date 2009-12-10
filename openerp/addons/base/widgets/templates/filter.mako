<input type="hidden" id="search_view_id" value="${search_view_id}"/>
<input type="hidden" id="search_view" value="${search_view}"/>
<table>
	<tr>
		<td class=label>
			${text_val}:
		</td>
		<td>
			<input ${py.attrs(attrs)} 
					type="checkbox"
					id="${filter_id}"
					name="${filter_id}"
					class="checkbox grid-domain-selector" 
					onclick="search_filter(this);" 
					value="${filter_domain}"
					title="${help}">
			</input>
		</td>
	</tr>
</table>
