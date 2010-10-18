% if editable:
    <input ${py.attrs(attrs)}
        type="hidden" 
        kind="${kind}" 
        name="${name}" 
        id="${name}" 
        value="${value}">
% endif

% if editable:
    <input ${py.attrs(attrs)}
        type="checkbox" 
        kind="${kind}" 
        class="checkbox"
        id="${name}_checkbox_" 
        ${py.checker(value)}>
% endif

% if editable and error:
    <span class="fielderror">${error}</span>
% endif

% if not editable:
    <input
        type="checkbox"
        kind="${kind}"
        class="checkbox" 
        id="${name}" 
        value="${value}" 
        ${py.checker(value)}
        disabled="disabled">
% endif

