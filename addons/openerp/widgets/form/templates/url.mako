% if editable:
    <table width="100%" border="0" cellpadding="0" cellspacing="0">
        <tr>
            <td style="padding: 0;">
                <input type="text" id="${name}" name="${name}" class="${css_class}"
                    ${py.attrs(attrs, kind=kind, value=value)}/>
            </td>
            <td width="16" style="padding-left: 10px">
                <img width="16" height="16" alt="${_('Go!')}" 
                    src="/openerp/static/images/stock/gtk-jump-to.png" 
                    style="cursor: pointer;" 
                    onclick="open_url(openobject.dom.get('${name}').value);"/>
            </td>
         </tr>
     </table>
    % if error:
    <span class="fielderror">${error}</span>
    % endif
% else:
    <a href="${value}">${value}</a>
% endif
