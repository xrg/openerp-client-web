<%inherit file="base.mako"/>

<%def name="header()">
    <title>OpenERP</title>
    <script type="text/javascript">
    
        var menubar, appbar, infobar = null
                
        MochiKit.DOM.addLoadEvent(function(evt){
        
            MochiKit.Iter.forEach(document.getElementsByTagName("a"), function(a){
                var v = getNodeAttribute(a, 'href');
                if (v.indexOf('/') == 0) {
                    a.target = "appFrame";
                }
            });
        
            menubar = getElement("menu_container");
            appbar = getElement("app_container");
            infobar = getElement("info_container");
            
            appbar.style.display = "none";
            infobar.style.display = "none";
        });
        
        var toggleMenubar = function() {
            
            if (menubar.style.display == "none")
                showMenuBar();
            else
                showAppBar();
        }
        
        var showMenuBar = function() {
            infobar.style.display = "none";
            appbar.style.display = "none";
            menubar.style.display = "";
        }
        
        var showAppBar = function() {
            menubar.style.display = "none";
            infobar.style.display = "none";
            appbar.style.display = "";
        }
        
        var showInfoBar = function() {
            menubar.style.display = "none";
            appbar.style.display = "none";
            infobar.style.display = "";
        }
        
    </script>
        
</%def>

<%def name="content()">

    <%include file="header.mako"/>
    
    <div id="info_container">
        <iframe width="100%" height="100%" border="0" frameborder="0" 
            id="infoFrame" name="infoFrame" src="${py.url('/info')}"></iframe>
    </div>

    <div id="app_container">
        <iframe width="100%" height="100%" border="0" frameborder="0" scrolling="no" 
            id="appFrame" name="appFrame" src=""></iframe>
    </div>

    <div id="menu_container">
        <iframe width="100%" height="100%" border="0" frameborder="0" scrolling="no" 
            id="menuFrame" name="menuFrame" src="${py.url('/menu')}"></iframe>
    </div>
    
    <%include file="footer.mako"/>
    
</%def>

