<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>${_("Select action")}</title>
</%def>

<%def name="content()">
<div class="view">

<script type="text/javascript">
    function onSubmit() {
        var form = openobject.dom.get('selection');
        var result = false;

        forEach(form._terp_action, function(e){
            result = result ? result : e.checked;
        });

        return result;
    }
</script>

<form id="selection" action="/openerp/selection/action" onsubmit="return onSubmit()">

    <input type="hidden" name="_terp_data" value="${data}"/>

    <div class="header">

        <div class="title">
            ${_("Select your action")}
        </div>

        <div class="spacer"></div>

            <table width="100%" border="0" class="fields">
                % for key, value in values.items():
                <tr>
                    <td width="25px"><input type="radio" id="_terp_action" name="_terp_action" value="${value}"/></td>
                    <td>${key}</td>
                </tr>
                % endfor
            </table>

        <div class="spacer"></div>

        <div class="toolbar">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td width="100%">
                    </td>
                    <td>
                    	<a class="button-a" href="javascript: void(0)" onclick="window.opener ? window.close() : history.back()">${_("Cancel")}</a>
                        <button type="submit">${_("OK")}</button>
                    </td>
                </tr>
            </table>
        </div>

    </div>
</form>

</div>
</%def>
