
<table>
	<tr>
		<td>
		% if def_checked:
				<div class="active-filter" onclick="if(this.className=='active-filter'){this.className='inactive-filter'}else {this.className='active-filter'} ;search_filter(getElement('${filter_id}'))" title="${help}">
					% if icon:
						<div align="center">
							<img src="${icon}" width="16" height="15"/>
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
				<div class="inactive-filter" onclick="if(this.className=='active-filter'){this.className='inactive-filter';}else {this.className='active-filter'} ;search_filter(getElement('${filter_id}'))" title="${help}">
					% if icon:
						<div align="center">
							<img src="${icon}" width="16" height="15"/>
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
