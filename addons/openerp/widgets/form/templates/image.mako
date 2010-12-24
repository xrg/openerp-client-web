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
        <img 
            id="${field}"
            name="${name}" 
            border='1' 
            alt="Click here to add new image." 
            align="left" 
            src=""
            width="100"
            height="100"
            class="${css_class} no_image"
            ${py.attrs(attrs)}
            onclick="openobject.tools.openWindow(openobject.http.getURL('/openerp/image', {model: '${model}', id: '${id}', field : '${field}'}), {width: 500, height: 300});" 
        />
    % endif
% else:
    % if id:
        <img
            id="${field}"
            name="${name}"
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
<input type="hidden" id="${name}" name="${name}" is_image="true" value="${src or bin_src or ''}"/>