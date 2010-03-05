<%inherit file="/openerp/controllers/templates/base.mako"/>

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
                    <button type='button' style="width: 80px" onclick="openobject.http.redirect('/')">${_("Cancel")}</button>
                    <button type='button' style="width: 80px" onclick="submit_form('ok')">${_("Save")}</button>
                </td>
            </table>
        </form>
    </div>
    
</%def>
