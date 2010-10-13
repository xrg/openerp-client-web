<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <script type="text/javascript">    
        jQuery(document).ready(function(){
            if (window.opener) {
                var $check_view = jQuery(window.opener.document).find('#_terp_view_type');
                
                if($check_view.length) {
                    var view = jQuery(window.opener.document).find('#_terp_view_type').val()
                    if(view == 'tree') {
                        new window.opener.ListView('_terp_list').reload()
                    }
                    
                    else {
                        var editable = jQuery(window.opener.document).find('#_terp_editable').val();
                        var form_action = 'save';
                        if(editable == 'True') {
                            form_action = 'save_and_edit';
                        }
                        window.opener.submit_form(form_action); 
                    }
                }
                else {
                    window.opener.location.reload();
                }
                window.close();
                
            } else {
            	window.location.href='/openerp';
            }
        });
    </script>
</%def>

<%def name="content()">

</%def>
