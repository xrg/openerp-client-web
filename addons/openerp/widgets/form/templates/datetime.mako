% if editable:
    <table cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0px;">
                <input type="text" id="${name}" name="${name}" 
                class="${css_class}" ${py.attrs(attrs, kind=kind, value=value)}/>
                % if error:
                <span class="fielderror">${error}</span>
                % endif
            </td>
            % if not attrs.get('disabled'):
            <td width="16" style="padding-left: 5px">
                <img id="${name}_trigger" width="16" height="16" alt="${_('Select')}" 
                src="/openerp/static/images/stock/stock_calendar.png" class="${css_class}" style="cursor: pointer;"/>
            </td>
            
            <script type="text/javascript">
                var dt_field = openobject.dom.select("[id='${name}']");
                var dt_button = openobject.dom.select("[id='${name}_trigger']");                
                dt_field = dt_field[dt_field.length-1];
                dt_button = dt_button[dt_button.length-1];
            
                Calendar.setup(
                {
                    inputField : dt_field,
                    ifFormat : "${format}",
                    button : dt_button,
                    showsTime: ${str(picker_shows_time).lower()}
                });
            </script>
            % endif
        </tr>
    </table>
% else:
    <span kind="${kind}" id="${name}" value="${value}">${value}</span>
% endif

