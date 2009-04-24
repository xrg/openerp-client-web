% if editable:
    <table width="100%" border="0" cellpadding="0" cellspacing="0">
        <tr>
            <td>
                <input type="text" id="${name}" name="${name}" class="${css_class}"
                    ${py.attrs(attrs, kind=kind, value=value)}/>
            </td>
            <td width="16" style="padding-left: 2px">
                <img width="16" height="16" alt="${_('Go!')}" 
                     src="/static/images/stock/gtk-jump-to.png" 
                     style="cursor: pointer;" 
                     onclick="if (validate_email($('${name}').value)) window.open('mailto:' + $('${name}').value).close();"/>
            </td>
        </tr>
    </table>
    % if error:
    <span class="fielderror">${error}</span>
    % endif
% else:
    <a href="mailto: ${value}">${value}</a>
% endif

