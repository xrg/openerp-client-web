<div class="filter-switch ${def_checked and 'active_filter' or 'inactive_filter'}"
     onclick="search_filter(getElement('${filter_id}'), this);" title="${help}">
    % if icon:
        <div>
            <img src="${icon}" width="16" height="16" alt=""/>
        </div>
    % endif
    % if help != text_val:
        ${text_val}
    % endif
    <input ${py.attrs(attrs)} style="display:none;"
        type="checkbox"
        id="${filter_id}"
        name="${filter_id}"
        class="checkbox grid-domain-selector"
        onclick="search_filter(this);"
        value="${filter_domain}"
        group_by_ctx="${group_context}"
        ${def_checked and 'checked' or ''}
        title="${help}" />
</div>
