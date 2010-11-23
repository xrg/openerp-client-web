<!doctype html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link rel="shortcut icon" href="/openobject/static/images/favicon.ico">
    
    <link type="text/css" rel="stylesheet" href="/openobject/static/css/jquery-ui/smoothness/jquery-ui-1.8.6.custom.css"/>
    <link type="text/css" rel="stylesheet" href="/openobject/static/css/jquery.fancybox-1.3.1.css"/>

% for css in widget_css:
    ${css.display()}
% endfor

    <script type="text/javascript" src="/openobject/static/javascript/MochiKit.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/MochiKit/Resizable.js"></script>

    <script type="text/javascript" src="/openobject/static/javascript/jQuery/jquery-1.4.2.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/jQuery/jquery-ui-1.8.6.custom.min.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/jQuery/jquery.form.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/jQuery/jquery.ba-hashchange.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/jQuery/jquery.fancybox-1.3.1.js"></script>
    
    <script type="text/javascript">
        jQuery.noConflict();
    </script>
    
    <script type="text/javascript" src="/openobject/static/javascript/openobject/openobject.base.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/openobject/openobject.gettext.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/openobject/openobject.dom.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/openobject/openobject.http.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/openobject/openobject.tools.js"></script>
    
    <script type="text/javascript">
        window.SCRIPT_PATH = "${cp.request.app.script_name}";
        openobject.http.SCRIPT_PATH = "${cp.request.app.script_name}";
    </script>
    
% for js in widget_javascript.get('head', []):
    ${js.display()}
% endfor
 
    ${next.header()}

</head>

<body>

% for js in widget_javascript.get('bodytop', []):
    ${js.display()}
% endfor


${self.content()}


% for js in widget_javascript.get('bodybottom', []):
    ${js.display()}
% endfor

</body>
</html>
