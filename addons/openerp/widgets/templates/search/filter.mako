<div class="filter-a">
	<%
		if def_checked:
			filter_class = "active_filter"
			a_class = "active"
		else:
			filter_class = "inactive_filter"
			a_class = "inactive"
			
		if help != text_val:
			text = text_val
			ul_class="filter_with_icon"
		else:
			text = ''
			ul_class="filter_icon"
	%>
	
	<button type="button" class="${ul_class} ${a_class}" title="${help}" onclick="search_filter(jQuery('#${filter_id}'), this);">
       % if icon:
           <img src="${icon}" width="16" height="16" alt="">
       % endif
       % if text:
           ${text}
       % endif
	</button>
    <input ${py.attrs(attrs)} style="display:none;"
        type="checkbox"
        id="${filter_id}"
        name="${filter_id}"
        class="grid-domain-selector"
        onclick="search_filter(this);"
        value="${filter_domain}"
        group_by_ctx="${group_context}"
        title="${help}" filter_context="${filter_context}"
        ${'checked' if def_checked else ''}/>
</div>
