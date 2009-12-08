<%inherit file="base.mako"/>

<%def name="header()">
    <script type="text/javascript">    
        MochiKit.DOM.addLoadEvent(function(evt){
        
            var frame = window.frameElement ? window.frameElement.name : null;
            
            if (frame == "appFrame") {
                window.location.href = "about:blank";
                return parent.setTimeout("showMenuBar()", 0);
            }
        
            if (window.opener) {
                window.opener.setTimeout("window.location.reload()", 0);
                window.close();
            } else {
                openobject.http.redirect('/');
            }
        });
    </script>
</%def>

<%def name="content()">

</%def>
