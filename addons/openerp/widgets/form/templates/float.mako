% if editable:
    <input 
        type="text" 
        kind="${kind}" 
        name='${name}' 
        id ='${name}' 
        value="${value}" 
        size="1"
        class="${css_class}" ${py.attrs(attrs, fld_required=required and 1 or 0, fld_readonly=readonly and 1 or 0)}/>
% endif

% if editable and error:
    <span class="fielderror">${error}</span>
% endif

% if not editable:
    <span kind="${kind}" id="${name}" value="${value}">${value}</span>
% endif

