% if editable:
    <input ${py.attrs(attrs)}
        type="hidden" 
        kind="${kind}" 
        name="${name}" 
        id="${name}" 
        value="${value}"/>
% endif

% if editable:
    <input ${py.attrs(attrs)}
        type="checkbox" 
        kind="${kind}" 
        class="checkbox"
        id="${name}_checkbox_" 
        checked="${(value or None) and 1}" 
        onclick="onBooleanClicked('${name}')"/>
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
        checked="${(value or None) and 1}" 
        disabled="disabled"/>
% endif

