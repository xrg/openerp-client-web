<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>${params.string}</title>
    <script type="text/javascript">
        var form_controller = '/openerp/pref';
        
        function clear_cache() {
        	window.location.href = "${py.url('/openerp/pref/clear_cache')}";
        }
    </script>
</%def>

<%def name="content()">

    <div class="view">
        <form name="view_form" id="view_form" action="/openerp/pref/ok" method="post">
            <table align="center">
                <tr>
                    <td class="toolbar welcome">${params.string}</td>
                </tr>
                <tr>
                    <td>${form.display()}</td>
                </tr>

                <tr>
	                <td style="text-align: right; padding: 0 30px 0 0;">
	                	% if environment == 'production':
	                		<button type="button" id="cache_clear" name="cache_clear" onclick="clear_cache();">Clear Cache</button>
	                	% endif
	                    <button type='button' class="static_buttons" onclick="openobject.http.redirect('/openerp')">${_("Cancel")}</button>
	                    <button type='button' class="static_buttons" onclick="submit_form('ok')">${_("Save")}</button>
	                </td>
	            </tr>
            </table>
        </form>
    </div>
    
</%def>
