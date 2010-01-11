<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    
% for css in widget_css:
    ${css.display()}
% endfor

    <script type="text/javascript" src="/openobject/static/javascript/MochiKit/MochiKit.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/MochiKit/DragAndDrop.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/MochiKit/Resizable.js"></script>

    <script type="text/javascript" src="/openobject/static/javascript/MochiKit/Resizable.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/MochiKit/Sortable.js"></script>
    
    <script type="text/javascript" src="/openobject/static/javascript/Sizzle/sizzle.js"></script>
    
    <script type="text/javascript" src="/openobject/static/javascript/openobject/openobject.base.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/openobject/openobject.gettext.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/openobject/openobject.dom.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/openobject/openobject.http.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/openobject/openobject.tools.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/openobject/openobject.ui.js"></script>
    
    <script type="text/javascript">
        window.SCRIPT_PATH = "${cp.request.app.script_name}";
        openobject.http.SCRIPT_PATH = "${cp.request.app.script_name}";
    </script>
    
    <script type="text/javascript" src="/openerp/static/javascript/ajax_stat.js"></script>
    
% for js in widget_javascript.get('head', []):
    ${js.display()}
% endfor

    <link rel="stylesheet" type="text/css" href="/openerp/static/css/style.css"/>
    <link rel="stylesheet" type="text/css" href="/openerp/static/css/menu.css"/>
    <link rel="stylesheet" type="text/css" href="/openerp/static/css/tips.css"/>

    <!--[if IE]>
    <link rel="stylesheet" type="text/css" href="/openobject/static/css/style-ie.css"/>
    <![endif]-->
    
    <script type="text/javascript" src="/openerp/static/javascript/menu.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/openobject/openobject.ui.tips.js"></script>
    
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
