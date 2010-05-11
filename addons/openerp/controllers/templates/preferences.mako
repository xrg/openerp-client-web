<%inherit file="/openerp/controllers/templates/xhr.mako"/>

<%def name="header()">
    <title>${params.string}</title>
    <script type="text/javascript">
        var form_controller = '/pref';
    </script>
</%def>

<%def name="content()">

    <div class="view">
        <form name="view_form" id="view_form" action="/pref/ok" method="post">
            <table align="center">
                <tr>
                    <td class="toolbar welcome">${params.string}</td>
                </tr>
                <tr>
                    <td>${form.display()}</td>
                </tr>
                <td class="toolbar" align="right">
                	% if environment == 'production':
                		<a class="button" id="cache_clear" href="${py.url('/pref/clear_cache')}">Clear Cache</a>
                	% endif
                    <a class="button" style="width: 80px" href="about:blank">${_("Cancel")}</a>
                    <button type='button' style="width: 80px" onclick="submit_form('ok')">${_("Save")}</button>
                </td>
            </table>
        </form>
    </div>
    
</%def>
