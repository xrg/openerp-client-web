<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    
% for css in widget_css:
    ${css.display()}
% endfor

    ${cp.static.js("base", "MochiKit/MochiKit.js")}
    ${cp.static.js("base", "MochiKit/DragAndDrop.js")}
    ${cp.static.js("base", "MochiKit/Resizable.js")}

    ${cp.static.js("base", "MochiKit/Resizable.js")}
    ${cp.static.js("base", "MochiKit/Sortable.js")}
    
    ${cp.static.js("base", "Sizzle/sizzle.js")}
    
    ${cp.static.js("base", "openobject/openobject.base.js")}
    ${cp.static.js("base", "openobject/openobject.gettext.js")}
    ${cp.static.js("base", "openobject/openobject.dom.js")}
    ${cp.static.js("base", "openobject/openobject.http.js")}
    ${cp.static.js("base", "openobject/openobject.tools.js")}
    ${cp.static.js("base", "openobject/openobject.links.js")}
    ${cp.static.js("base", "openobject/openobject.ui.js")}
    
    <script type="text/javascript">
        window.SCRIPT_PATH = "${cp.request.app.script_name}";
        openobject.http.SCRIPT_PATH = "${cp.request.app.script_name}";
    </script>
    
    ${cp.static.js("base", "javascript/ajax_stat.js")}
    
% for js in widget_javascript.get('head', []):
    ${js.display()}
% endfor

    ${cp.static.css("base", "style.css")}
    ${cp.static.css("base", "menu.css")}
    ${cp.static.css("base", "tips.css")}

    <!--[if IE]>
    ${cp.static.css("base", "style-ie.css")}
    <![endif]-->
    
    ${cp.static.js("base", "menu.js")}
    ${cp.static.js("base", "openobject/openobject.ui.tips.js")}
    
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
