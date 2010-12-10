% if editable:
    <select 
        id="${name}"
        kind="${kind}"
        name="${name}"
        type2 = "${type2}"
        operator="${operator}"
        class="${css_class}"
        search_context="${search_context}" ${py.attrs(attrs)}>
        ## add empty option only if no empty option exist
        ## and no default value is set
        % if all(label for _, label in options) and not value:
            <option value=""></option>
        % endif
        % for (val, label) in options:
            <option value="${val}" ${py.selector(val==(value or False))}>${label}</option>
        % endfor
    </select>
    % if error:
    <span class="fielderror">${error}</span>
    % endif
% else:
    <span kind="${kind}" id="${name}" value="${value}">${dict(options).get(value)}</span>
% endif

