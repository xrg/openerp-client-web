% if editable:
    <input type="text" id="${name}" name="${name}" class="${css_class}" size="1"
        ${py.attrs(attrs, kind=kind, value=value)}/>
    % if error:
    <span class="fielderror">${error}</span>
    % endif
% else:
    <a href="${value}" target="_blank">${value}</a>
% endif
