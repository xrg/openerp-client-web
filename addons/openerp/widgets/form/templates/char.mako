% if editable:
    <input type="${password and 'password' or 'text'}"
        id="${name}" name="${name}" class="${css_class}"
        ${py.attrs(attrs, kind=kind, maxlength=size, value=value)}/>
    % if error:
    <span class="fielderror">${error}</span>
    % endif
% elif not password:
    <span kind="${kind}" id="${name}">${value}</span>
% elif value:
    <span>${'*' * len(value)}</span>
% endif

