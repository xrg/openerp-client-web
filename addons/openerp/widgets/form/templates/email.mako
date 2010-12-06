% if editable:
    <input type="text" id="${name}" name="${name}" class="${css_class}" size="1"
        ${py.attrs(attrs, kind=kind, value=value)}/>
    % if error:
    <span class="fielderror">${error}</span>
    % endif
% else:
    <a style="color:#9A0404;" target="_self" href="mailto: ${value}">${value}</a>
% endif
