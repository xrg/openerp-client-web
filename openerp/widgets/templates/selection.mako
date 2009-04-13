% if editable:
    <select 
        id="${name}" 
        kind="${kind}" 
        name="${name}" 
        style="width: 100%" 
        class="${css_class}" ${py.attrs(attrs)}>
        <option value=""></option>
        % for (k, v) in options:
            % if value == k:
        <option value="${k}" selected="1">${v}</option>
            % endif
        % endfor
        % for (k, v) in options:
            % if value != k:
        <option value="${k}">${v}</option>
            % endif
        % endfor
    </select>
    % if error:
    <span class="fielderror">${error}</span>
    % endif
% else:
    <span kind="${kind}" id="${name}" value="${value}">${dict(options).get(value)}</span>
% endif

