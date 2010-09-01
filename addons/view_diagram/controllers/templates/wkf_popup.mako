<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${form.screen.string} </title>

    <script type="text/javascript">
        var form_controller = '${params.path}';

         function on_load() {

           	var id = parseInt(openobject.dom.get('_terp_id').value) || 0;

            var lc = openobject.dom.get('_terp_load_counter').value;
            lc = parseInt(lc) || 1;

            if (lc > 1) {

                if (id != 0) {
            	    window.opener.setTimeout("WORKFLOW.${params.function}"+"("+id+")", 0);
               }

               return window.close();
            }
        }

        jQuery(document).ready(on_load);
    </script>
</%def>

<%def name="content()">
    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <input type="hidden" id="_terp_load_counter" value="${params.load_counter or 0}"/>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="100%"><h1>${form.screen.string}</h1>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                        	<td style="padding: 0 2px 0 10px;">
                                <a class="button-a" href="javascript: void(0)" onclick="submit_form('save')">${_("Save")}</a>
                            </td>
                            <td style="padding: 0 2px 0 0px;">
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
