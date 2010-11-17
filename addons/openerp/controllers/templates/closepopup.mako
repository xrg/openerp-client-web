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
                    var $dialog = jQuery(topWindow.document).find('.action-dialog');
                    $dialog.dialog('close');
                });
            } else {
                topWindow = window.opener;
                setTimeout(close);
            }
            var $doc = jQuery(topWindow.document);
            switch($doc.find('#_terp_view_type').val()) {
                case null:
                case undefined:
                    topWindow.location.reload();
                    return;
                case 'tree':
                    new topWindow.ListView('_terp_list').reload();
                    return;
            }
            var form_action = 'save';
            if($doc.find('#_terp_editable').val() == 'True') {
                form_action = 'save_and_edit';
            }
            topWindow.submit_form(form_action);
        });
    </script>
</%def>

<%def name="content()">

</%def>
