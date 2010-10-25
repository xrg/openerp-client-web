<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${_("Server Actions...")}</title>
    <link href="/openerp/static/css/style.css" rel="stylesheet" type="text/css"/>
</%def>

<%def name="content()">
    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="100%"><h1>${_("Server Actions")}</h1></td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                % for log in serverLog:
	    			<div class="logActions">
    					<a href="${py.url('/openerp/form/edit', model=log['res_model'], id=log['res_id'])}">
    						${log['name']}
    					</a>
	    			</div>
	    		% endfor
            </td>
        </tr>
    </table>
</%def>