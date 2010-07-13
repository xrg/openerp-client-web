% if editable:
    <input type="text" id="${name}" name="${name}" 
    class="${css_class}" ${py.attrs(attrs, kind=kind, value=value)}/>
    % if error:
    <span class="fielderror">${error}</span>
    % endif

    % if not attrs.get('disabled'):
    <script type="text/javascript">
        Calendar.setup(
        {
            inputField : jQuery("[id='${name}']").get(0),
            ifFormat : "${format}",
            showsTime: ${str(picker_shows_time).lower()}
        });
    </script>
    % endif
% else:
    <span kind="${kind}" id="${name}" value="${value}">${value}</span>
% endif
