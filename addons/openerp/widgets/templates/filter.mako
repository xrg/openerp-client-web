<div class="filter-a">
	<%
		if def_checked:
			filter_class = "active_filter"
			a_class = "active"
			checked_default = "true"
		else:
			filter_class = "inactive_filter"
			a_class = "inactive"
			checked_default = "false"
			
		if help!=text_val:
			text = text_val
			ul_class="filter_with_icon"
		else:
			text = ''
			ul_class="filter_icon"
	%>
	<ul class="${ul_class}">
		<li class="${filter_class}" title="${help}" onclick="search_filter(getElement('${filter_id}'), this);">
			<a class="${a_class}" style="background-image: url(${icon});">
				% if text:
				    ${text}
				% endif
				<span>&raquo;</span>
				<input ${py.attrs(attrs)} style="display:none;"
                    type="checkbox"
                    id="${filter_id}"
                    name="${filter_id}"
                    class="grid-domain-selector"
                    onclick="search_filter(this);"
                    value="${filter_domain}"
                    group_by_ctx="${group_context}"
                    title="${help}" filter_context="${filter_context}"/>
			</a>
		</li>
	</ul>
</div>
