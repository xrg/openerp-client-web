<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${form.screen.string}</title>

    <script type="text/javascript">
        var form_controller = '/openerp/viewed/new_model';

        function do_select(id, src) {
            viewRecord(id, src);
        }

        var createNewModel = function() { 
            openLink(get_form_action('edit')); 
        }
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
                            	<a class="button-a" href="javascript: void(0)" onclick="createNewModel()">${_("New")}</a>
                            </td>
                            <td class="save_close">
                           		<a class="button-a" href="javascript: void(0)" onclick="submit_form('save_and_edit')">${_("Save")}</a>
                            </td>
                            <td class="save_close">
                            	<a class="button-a" href="javascript: void(0)" onclick="window.close()">${_("Close")}</a>
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
