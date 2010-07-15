% if editable:
<table class="item-wrapper">
<tr>
    <td>
        <input type="text" id="${name}" name="${name}" 
        class="${css_class}" ${py.attrs(attrs, kind=kind, value=value)}/>
        % if error:
        <span class="fielderror">${error}</span>
        % endif
    </td>
    % if not attrs.get('disabled'):
    <td class="item-image">
        <img id="${name}_trigger" width="16" height="16" alt="${_('Select')}" 
            src="/openerp/static/images/stock/stock_calendar.png"
            class="${css_class}" style="cursor: pointer;"/>
            
        <script type="text/javascript">
            Calendar.setup(
            {
                inputField : jQuery("[id='${name}']").last().get(0),
                ifFormat : "${format}",
                button : jQuery("[id='${name}_trigger']").last().get(0),
                showsTime: ${str(picker_shows_time).lower()}
            });
        </script>
    </td>
    % endif
</tr>
</table>
% else:
    <span kind="${kind}" id="${name}" value="${value}">${value}</span>
% endif
