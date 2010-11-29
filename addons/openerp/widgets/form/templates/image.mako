% if editable:
    % if src:
        <img 
            id="${field}"
            name="${name}" 
            border='1' 
            alt="Click here to add new image." 
            align="left" 
            src="${src}" 
            % if width:
                width="${width}"
            % endif
            % if height:
                height="${height}"
            % endif
            ${py.attrs(attrs)}
            onclick="openobject.tools.openWindow(openobject.http.getURL('/openerp/image', {model: '${model}', id: '${id}', field : '${field}'}), {width: 500, height: 300});" 
        />
    % elif bin_src:
        <img
            src="data:image/png;base64,${bin_src}"
            class="${css_class}"
            id="${field}"
            name="${name}"
            % if width:
                width="${width}"
            % endif
            % if height:
                height="${height}"
            % endif
            ${py.attrs(attrs)}
            onclick="openobject.tools.openWindow(openobject.http.getURL('/openerp/image', {model: '${model}', id: '${id}', field : '${field}'}), {width: 500, height: 300});"
        />
    % else:
        <input type="file" class="${css_class}" id="${name}" ${py.attrs(attrs)} name="${name}"/>
    % endif
% else:
    % if id:
        <img
            id="${field}"
            border='1'
            align="left"
            src="${src}"
            % if width:
                width="${width}"
            % endif
            % if height:
                height="${height}"
            % endif
        />
    % else:
        % if src:
            <img
                src="data:image/png;base64,${src}"
                class="${css_class}"
                id="${name}"
                ${py.attrs(attrs)}
                name="${name}"
                % if width:
                    width="${width}"
                % endif
                % if height:
                    height="${height}"
                % endif
            />
        % elif bin_src:
            <img
                src="data:image/png;base64,${bin_src}"
                class="${css_class}"
                id="${name}"
                ${py.attrs(attrs)}
                name="${name}"
                % if width:
                    width="${width}"
                % endif
                % if height:
                    height="${height}"
                % endif
            />
        % endif
        
    % endif
% endif
<input type="hidden" id="_${field}" name="${name}" value="${src or bin_src or ''}">
