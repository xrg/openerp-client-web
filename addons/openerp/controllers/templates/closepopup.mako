<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <script type="text/javascript">    
        jQuery(document).ready(function(){
            if(!window.opener && window.top == window) {
                window.location.href = '/openerp';
                return;
            }
            var topWindow;
            if(window.top != window) {
                topWindow = window.top;
                setTimeout(function () {
                    topWindow.closeAction();
                });
            } else {
                topWindow = window.opener;
                setTimeout(close);
            }
            /*
            % if reload:
            */
            var $doc = jQuery(topWindow.document);
            switch($doc.find('#_terp_view_type').val()) {
                case 'tree':
                    new topWindow.ListView('_terp_list').reload();
                    return;
            }
            topWindow.location.reload();
            /*
            % endif
            */
        });
    </script>
</%def>

<%def name="content()">

</%def>
