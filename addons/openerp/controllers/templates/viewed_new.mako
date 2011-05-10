<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${form.screen.string}</title>

    <script type="text/javascript">
        var form_controller = '/openerp/viewed/new_field';
    </script>

    <script type="text/javascript">
        jQuery(document).ready(function() {

            var lc = parseInt(jQuery('#_terp_id').val(), 10) || 0;

            if (lc > 0) {
               window.top.jQuery(window.frameElement).data('source-window').addNewFieldName(jQuery('#name').val());
               window.frameElement.close();
            }
        });
    </script>
</%def>

<%def name="content()">
    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="100%"><h1>${form.screen.string}</h1></td>
                    </tr>
                </table>
            </td>
        </tr> 
        <tr>
            <td>
                <div class="footer_tool_box">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td class="save_close">
                            	<a class="button-a" href="javascript: void(0);" onclick="submit_form('save');">${_("Save")}</a>
                            </td>
                            <td class="save_close">
                            	<a class="button-a" href="javascript: void(0);" onclick="window.frameElement.close();">${_("Close")}</a>
                            </td>
                            <td width="100%">
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
        <tr>
            <td>${form.display()}</td>
        </tr>
    </table>
</%def>
