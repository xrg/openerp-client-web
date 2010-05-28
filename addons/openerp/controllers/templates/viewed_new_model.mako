<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>${form.screen.string}</title>

    <script type="text/javascript">
        var form_controller = '/openerp/viewed/new_model';
    </script>
    
    <script type="text/javascript">

        function do_select(id, src) {
            viewRecord(id, src);
        }

        var createNewModel = function() { 
            window.location.href = get_form_action('edit'); 
        }
    </script>
</%def>

<%def name="content()">
    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="100%">${form.screen.string}</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>${form.display()}</td>
        </tr>
        <tr>
            <td>
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td>
                            	<a class="button-a" href="javascript: void(0)" onclick="createNewModel()">${_("New")}</a>
                            </td>
                            <td width="100%"></td>
                            <td>
                            	<a class="button-a" href="javascript: void(0)" onclick="window.close()">${_("Close")}</a>
                           	</td>
                           	<td>
                           		<a class="button-a" href="javascript: void(0)" onclick="submit_form('save_and_edit')">${_("Save")}</a>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</%def>
