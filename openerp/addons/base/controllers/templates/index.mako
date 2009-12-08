<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>OpenERP</title>
    
    <link href="${cp.static('base', 'css/style.css')}" rel="stylesheet" type="text/css"/>
    
    <script type="text/javascript">
        window.SCRIPT_PATH = "${cp.request.app.script_name}";
    </script>

    <script type="text/javascript" src="${cp.static('base', 'javascript/MochiKit/MochiKit.js')}"></script>   
    
    <script type="text/javascript">
    
        var menuFrame, appFrame = null;
        var container = null;
        
        MochiKit.DOM.addLoadEvent(function(evt){
        
            menuFrame = getElement("menuFrame");
            appFrame = getElement("appFrame");
            
            container = getElement("frameContainer");

        });
        
        var toggleMenubar = function() {
        
            var current = getCurrentFrame();
                        
            if (appFrame.contentWindow.location.href == "about:blank") {
                return showMenuBar();
            }
            
            return current == menuFrame ? showAppBar() : showMenuBar();
        }
        
        var getCurrentFrame = function() {
            switch(container.rows) {
                case "*,100%":
                    return appFrame;
                case "100%,*":
                    return menuFrame;
            }
        }
        
        var showMenuBar = function() {
            container.rows = "100%,*";
            return menuFrame;
        }
        
        var showAppBar = function() {
            container.rows = "*,100%";
            return appFrame;
        }
        
    </script>
</head>

    <frameset id="frameContainer" border="0" frameborder="0" rows="100%,*">
        <frame id="menuFrame" name="menuFrame" target="appFrame" src="${py.url('/menu')}"/>
        <frame id="appFrame" name="appFrame" src=""/>
    </frameset>
    
</html>
