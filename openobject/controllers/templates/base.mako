<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    
% for css in widget_css:
    ${css.display()}
% endfor

    ${cp.static.js("openobject", "MochiKit/MochiKit.js")}
    ${cp.static.js("openobject", "MochiKit/DragAndDrop.js")}
    ${cp.static.js("openobject", "MochiKit/Resizable.js")}

    ${cp.static.js("openobject", "MochiKit/Resizable.js")}
    ${cp.static.js("openobject", "MochiKit/Sortable.js")}
    
    ${cp.static.js("openobject", "Sizzle/sizzle.js")}
    
    ${cp.static.js("openobject", "openobject/openobject.base.js")}
    ${cp.static.js("openobject", "openobject/openobject.gettext.js")}
    ${cp.static.js("openobject", "openobject/openobject.dom.js")}
    ${cp.static.js("openobject", "openobject/openobject.http.js")}
    ${cp.static.js("openobject", "openobject/openobject.tools.js")}
    ${cp.static.js("openobject", "openobject/openobject.links.js")}
    ${cp.static.js("openobject", "openobject/openobject.ui.js")}
    
    <script type="text/javascript">
        window.SCRIPT_PATH = "${cp.request.app.script_name}";
        openobject.http.SCRIPT_PATH = "${cp.request.app.script_name}";
    </script>
    
    ${cp.static.js("openerp", "javascript/ajax_stat.js")}
    
% for js in widget_javascript.get('head', []):
    ${js.display()}
% endfor

    ${cp.static.css("openerp", "style.css")}
    ${cp.static.css("openerp", "menu.css")}
    ${cp.static.css("openerp", "tips.css")}

    <!--[if IE]>
    ${cp.static.css("openobject", "style-ie.css")}
    <![endif]-->
    
    ${cp.static.js("openerp", "menu.js")}
    ${cp.static.js("openobject", "openobject/openobject.ui.tips.js")}
    
    ${self.header()}

</head>

<body>

% for js in widget_javascript.get('bodytop', []):
    ${js.display()}
% endfor

<div id="content_container">
${self.content()}
</div>

% for js in widget_javascript.get('bodybottom', []):
    ${js.display()}
% endfor

</body>
</html>
