% if editable:
    <input type="text" id="${name}" name="${name}" class="${css_class}"
        ${py.attrs(attrs, kind=kind, value=value)}/>
    % if error:
    <span class="fielderror">${error}</span>
    % endif
% else:
    <a href="${value}">${value}</a>
% endif
