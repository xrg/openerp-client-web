% if editable:
    % if inline:
        <input id ="${name}" name="${name}" type="text" class="${css_class}" size="1"
            ${py.attrs(attrs, kind=kind, value=value)}/>
    % else:
        <textarea rows="6" id ="${name}" name="${name}" class="${css_class}"
            ${py.attrs(attrs, kind=kind)} style="width: 99%;">${value}</textarea>
        <script type="text/javascript">
            if (!window.browser.isWebKit) {
                new openerp.ui.TextArea('${name}');
            }
        </script>
    % endif

    % if error:
        <span class="fielderror">${error}</span>
    % endif
% else:
    <p kind="${kind}" id="${name}" class="raw-text">${value}</p>
% endif

