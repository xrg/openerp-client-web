% if editable:
    <input 
        type="hidden" 
        kind="${kind}" 
        name='${name}' 
        id='${name}' 
        relation="${relation}" 
        value="${value}" 
        class="${css_class}" ${py.attrs(attrs)}/>
% endif

