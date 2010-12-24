<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${form.screen.string} </title>

    <script type="text/javascript">
        var form_controller = '/openerp/openo2m';
        function do_select(id, src) {
            viewRecord(id, src);
        }
    </script>
</%def>

<%def name="content()">
    <table class="view" cellspacing="5" border="0" width="100%" style="border: none;">
        <tr>
            <td>
                <input type="hidden" id="_terp_load_counter" value="${params.load_counter}"/>
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
                                    <button onclick="submit_form('save'); return false;" style="height: 20px;" class="button-a">${_("Save")}</button>
	                            </td>
                            % endif
                            <td class="save_close">
                            	<button class="button-a" style="height: 20px;" onclick="jQuery.o2m('close'); return false;">${_("Close")}</button>
                            </td>
                            <td width="100%">
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
        <tr>
            <td style="padding: 2px 5px 5px;">${form.display()}</td>
        </tr>
    </table>
    <script type="text/javascript">
        jQuery('form').submit(function () {
            jQuery('.save_close:eq(0) button').attr('disabled', true);
        });
        jQuery.o2m('init');
    </script>
</%def>
