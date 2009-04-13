% if editable:
    <input type="${password and 'password' or 'text'}" \
           kind="${kind}" 
           name='${name}' 
           id='${field_id}' 
           value="${value}" 
           maxlength="${size}" 
           class="${css_class}"
           ${py.attrs(attrs)}/>
    % if error:
    <span class="fielderror">${error}</span>
    % endif
% endif

% if not editable and not password:
    <span kind="${kind}" id="${name}">${value}</span>
% endif

% if not editable and password and value:
    <span>${'*' * len(value)}</span>
% endif

