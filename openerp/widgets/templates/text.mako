% if editable and not inline:
<textarea rows="6" id ="${name}" name="${name}" 
    class="${css_class}" kind="${kind}"
    ${py.attrs(attrs)}>${value}</textarea>
% endif

% if editable and not inline:
<script type="text/javascript">
    if (!window.browser.isWebKit) {
        new ResizableTextarea('${name}');
    }
</script>
% endif

% if editable and inline:
<input id ="${name}" name="${name}"
    type="text" class="${css_class}" kind="${kind}"
    value="${value or None}"
    ${py.attrs(attrs)}/>
% endif

% if editable and error:
<span class="fielderror">${error}</span>
% endif

% if not editable and value:
<span kind="${kind}" id="${name}">
    % for line in value.split('\n'):
    <br>${line}</br>
    % endfor
</span>
% endif

