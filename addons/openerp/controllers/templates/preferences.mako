<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <script type="text/javascript">
    	document.title = '${params.string}' + ' - OpenERP';
        var form_controller = '/openerp/pref';
    </script>
</%def>

<%def name="content()">

    <div class="view">
        <form name="view_form" id="view_form" action="/openerp/pref/ok" method="post">
            <table align="center" style="border: none;">
                <tr>
                    <td class="error_message_header">${params.string}</td>
                </tr>
                <tr>
                    <td>${form.display()}</td>
                </tr>
                <tr>
	                <td style="text-align: right; padding: 0 30px 0 0;">
	                    <button type='button' class="static_boxes" onclick="openobject.http.redirect('/openerp')">${_("Cancel")}</button>
	                    <button type='button' class="static_boxes" onclick="submit_form('ok')">${_("Save")}</button>
	                </td>
	            </tr>
            </table>
        </form>
    </div>
    
</%def>
