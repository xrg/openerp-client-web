% if editable:
    <select 
        id="${name}" 
        kind="${kind}" 
        name="${name}" 
        class="${css_class}"
        search_context="${search_context}" ${py.attrs(attrs)}>
        <option value=""></option>
        % for (k, v) in options:
        <option value="${k}" ${py.selector(k==value)}>${v}</option>
        % endfor
    </select>
    % if error:
    <span class="fielderror">${error}</span>
    % endif
% else:
    <span kind="${kind}" id="${name}" value="${value}">${dict(options).get(value)}</span>
% endif

