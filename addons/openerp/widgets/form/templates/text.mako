% if editable and not inline:
<textarea rows="6" id ="${name}" name="${name}" class="${css_class}"
    ${py.attrs(attrs, kind=kind)} style="width: 99%;">${value}</textarea>
% endif

% if editable and not inline:
<script type="text/javascript">
    if (!window.browser.isWebKit) {
        new openerp.ui.TextArea('${name}');
    }
</script>
% endif

% if editable and inline:
<input id ="${name}" name="${name}" type="text" class="${css_class}"
    ${py.attrs(attrs, kind=kind, value=value)}/>
% endif

% if editable and error:
<span class="fielderror">${error}</span>
% endif

% if not editable:
<span kind="${kind}" id="${name}">
    % if value:
        % for line in value.split('\n'):
        <br>${line}</br>
        % endfor
    % endif
</span>
% endif

