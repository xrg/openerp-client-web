<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    
% for css in widget_css:
    ${css.display()}
% endfor

    <script type="text/javascript" src="${py.url('/static/javascript/MochiKit/MochiKit.js')}"></script>
    <script type="text/javascript" src="${py.url('/static/javascript/MochiKit/DragAndDrop.js')}"></script>
    <script type="text/javascript" src="${py.url('/static/javascript/MochiKit/Resizable.js')}"></script>
    <script type="text/javascript" src="${py.url('/static/javascript/MochiKit/Sortable.js')}"></script>
    
    <script type="text/javascript" src="${py.url('/static/javascript/Sizzle/sizzle.js')}"></script>
    
    <script type="text/javascript" src="${py.url('/static/javascript/openobject/openobject.base.js')}"></script>
    <script type="text/javascript" src="${py.url('/static/javascript/openobject/openobject.dom.js')}"></script>
    <script type="text/javascript" src="${py.url('/static/javascript/openobject/openobject.tools.js')}"></script>
    <script type="text/javascript" src="${py.url('/static/javascript/openobject/openobject.http.js')}"></script>
    
    <script type="text/javascript">
        window.SCRIPT_PATH = "${cp.request.app.script_name}";
        openobject.http.SCRIPT_PATH = "${cp.request.app.script_name}";
    </script>
    
% for js in widget_javascript.get('head', []):
    ${js.display()}
% endfor

    <link href="${py.url('/static/css/style.css')}" rel="stylesheet" type="text/css"/>
    <link href="${py.url('/static/css/menu.css')}" rel="stylesheet" type="text/css"/>
    <link href="${py.url('/static/css/tips.css')}" rel="stylesheet" type="text/css"/>

    <!--[if IE]>
    <link href="${py.url('/static/css/style-ie.css')}" rel="stylesheet" type="text/css"/>
    <![endif]-->
    
    <script type="text/javascript" src="${py.url('/static/javascript/menu.js')}"></script>
    <script type="text/javascript" src="${py.url('/static/javascript/tips.js')}"></script>
    
    <script type="text/javascript">
        
        MochiKit.DOM.addLoadEvent(function(evt){
            (function(){
            
                var frame = window.frameElement ? window.frameElement.name : null;
            
                if (frame == "appFrame") {
                    parent.setTimeout("showAppBar()", 0);
                }
                
                if (frame == "menuFrame") {
                                
                    var links = [];
                                        
                    links = openobject.dom.select("#header a, #footer a");
                    
                    forEach(links, function(a) {
                        if (!a.target) {
                            a.target = "appFrame";
                        }
                    });
                }
                
            })()
        });
    </script>
    
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
