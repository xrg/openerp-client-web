% if stock:
    <img align="left" src="${src}" width="${width}" height="${height}"/>
% endif

% if not stock and id and editable and kind=="picture":
    <img id="${field}" border='1' align="left" src="${src}" width="${width}" height="${height}"/>
% endif

% if not stock and id and editable and kind=="image":
    <img 
        id="${field}" 
        border='1' 
        alt="Click here to add new image." 
        align="left" 
        src="${src}" 
        width="${width}" 
        height="${height}" 
        onclick="openobject.tools.openWindow(openobject.http.getURL('/openerp/image', {model: '${model}', id: ${id}, field : '${field}'}), {width: 500, height: 300});"/>
% endif

% if not stock and id and not editable:
    <img id="${field}" border='1' align="left" src="${src}" width="${width}" height="${height}"/>
% endif

% if not stock and not id and editable:
    <input type="file" class="${css_class}" id="${name}" ${py.attrs(attrs)} name="${name}"/>
% endif

