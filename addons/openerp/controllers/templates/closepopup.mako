<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <script type="text/javascript">    
        jQuery(document).ready(function(){
            if (window.opener) {
                window.opener.location.reload();
                window.close();
            } else {
            	openobject.http.redirect('/openerp/blank');
            	window.parent.location.href = '/openerp/menu'; 
            }
        });
    </script>
</%def>

<%def name="content()">

</%def>
