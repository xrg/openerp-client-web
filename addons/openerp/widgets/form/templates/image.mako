% if stock:
    <img align="left" src="${src}" width="${width}" height="${height}"/>
% endif

% if not stock and id and editable and kind=="picture":
    <img id="${field}" border='1' align="left" src="${src}" width="${width}" height="${height}"/>
% endif
% if editable:
	% if img_size:
		% if src:
			<img 
	        id="${field}" 
	        border='1' 
	        alt="Click here to add new image." 
	        align="left" 
	        src="${src}" 
	        width="${width}" 
	        height="${height}" 
	        onclick="openobject.tools.openWindow(openobject.http.getURL('/openerp/image', {model: '${model}', id: '${id}', field : '${field}'}), {width: 500, height: 300});"/>
        % else:
        	<input type="file" class="${css_class}" id="${name}" ${py.attrs(attrs)} name="${name}" />
        % endif
	% else:
		<img 
		src="data:image/png;base64,${src}" 
		class="${css_class}" 
		id="${name}" 
		${py.attrs(attrs)} name="${name}"
		width="${width}" 
	    height="${height}" 
		onclick="openobject.tools.openWindow(openobject.http.getURL('/openerp/image', {model: '${model}', id: '${id}', field : '${field}'}), {width: 500, height: 300});"/>
		
	% endif
% else:
	% if id:
		<img id="${field}" border='1' align="left" src="${src}" width="${width}" height="${height}" onclick="openobject.tools.openWindow(openobject.http.getURL('/openerp/image', {model: '${model}', id: ${id}, field : '${field}'}), {width: 500, height: 300});"/>
	% else:
		<img src="data:image/png;base64,${src}" class="${css_class}" id="${name}" ${py.attrs(attrs)} name="${name}" width="${width}" height="${height}"/>
	% endif
% endif


