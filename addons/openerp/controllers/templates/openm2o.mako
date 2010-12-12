<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${form.screen.string} </title>

    <script type="text/javascript">
        var form_controller = '/openerp/openm2o';
    </script>

    <script type="text/javascript">
        
        function do_select(id, src) {
            viewRecord(id, src);
        }
        
        jQuery(document).ready(function() {
        
            var id = parseInt(openobject.dom.get('_terp_id').value, 10) || null;
            var lc = parseInt(openobject.dom.get('_terp_load_counter', 10).value) || 1;

            if(lc <= 1) {
                return;
            }
            $.m2o('close', id);
        });
    </script>
</%def>

<%def name="content()">
    <table class="view" cellspacing="5" border="0" width="100%" style="border: none;">
        <tr>
            <td style="padding: 0pt 2px 2px 5px;">
                <input type="hidden" id="_terp_load_counter" value="${params.load_counter or 0}"/>
                <table width="100%" class="titlebar" style="border: none;">
                    <tr>
                        <td width="100%"><h1>${form.screen.string}</h1></td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <div class="footer_tool_box">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border: none;">
                        <tr>
                        	% if form.screen.editable:
	                            <td class="save_close">
	                            	<a class="button-a" onclick="submit_form('save')" href="javascript: void(0)">${_("Save")}</a>
	                            </td>
                            % endif
                            <td class="save_close">
                            	<a class="button-a" onclick="$.m2o('close');" href="javascript: void(0)">${_("Close")}</a>
                            </td>
                            <td width="100%">
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
        <tr>
            <td style="padding: 5px;">${form.display()}</td>
        </tr>
    </table>
</%def>
