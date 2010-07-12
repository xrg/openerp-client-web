<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <script type="text/javascript">    
        jQuery(document).ready(function(){
            if (window.opener) {
                window.opener.location.reload();
                window.close();
            } else {
            	window.parent.location.href = '/openerp'; 
            }
        });
    </script>
</%def>

<%def name="content()">

</%def>
