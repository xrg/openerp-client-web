% if editable and not inline:
    <textarea rows="10" 
        id ="${name}"
        name="${name}"
        class="${css_class}" 
        kind="${kind}" ${py.attrs(attrs)}>${value or ''}</textarea>

    <script type="text/javascript">
        if (!window.browser.isWebKit) {
            new ResizableTextarea('${name}');
        }
    </script>
% endif

% if editable and inline:
    <input id="${name}" name="${name}"
        type="text" class="${css_class}" kind="${kind}"  
        value="${value or ''}" ${py.attrs(attrs)}/>
% endif
    
% if editable and error:
    <span class="fielderror">${error}</span>
% endif

% if not editable and value:
    <div kind="${kind}" id="${name}" class="${css_class}">${data | 'h'}</div>
% endif

