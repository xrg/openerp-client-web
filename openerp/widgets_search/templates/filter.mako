<input ${py.attrs(attrs)} 
		type="checkbox" 
		id="${filter_id}" 
		class="checkbox grid-domain-selector" 
		onclick="search_filter(this, this.value);" 
		value="${filter_domain}" 
		title="${help}">
	${text_val}
</input>
