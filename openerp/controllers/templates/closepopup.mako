<%! show_header_footer = False %>
<%inherit file="master.mako"/>

<%def name="header()">
    <script type="text/javascript">    
        MochiKit.DOM.addLoadEvent(function(evt){
            if (window.opener) {
                window.opener.setTimeout("window.location.reload()", 0);
                window.close();
            } else {
                doRedirect('/');
            }
        });
    </script>
</%def>

<%def name="content()">

</%def>
