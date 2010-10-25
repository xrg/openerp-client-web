% if editable:
    <input type="${password and 'password' or 'text'}"
        id="${name}" name="${name}" class="${css_class}"
        ${py.attrs(attrs, kind=kind, maxlength=size, value=value)}/>
    % if error:
    <span class="fielderror">${error}</span>
    % endif
% endif

% if not editable and not password:
    <span kind="${kind}" id="${name}" value="${value}">${value}</span>
% endif

% if not editable and password and value:
    <span>${'*' * len(value)}</span>
% endif

