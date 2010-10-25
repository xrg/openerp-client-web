<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${_("Select action")}</title>
</%def>

<%def name="content()">
<div class="view">

<script type="text/javascript">
    function onSubmit() {
        return jQuery('#selection input[name=_terp_action]:checked').length > 0;
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
                % for i, (key, value) in enumerate(values.iteritems()):
                <tr>
                    <td width="25px"><input type="radio" id="_terp_action_${i}" name="_terp_action" value="${value}"/></td>
                    <td><label for="_terp_action_${i}">${key}</label></td>
                </tr>
                % endfor
            </table>

        <div class="spacer"></div>

        <div class="toolbar">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td width="100%" align="right">
                        <button class="static_boxes" onclick="window.opener ? window.close() : history.back()">${_("Cancel")}</button>
                    <td>
                    	<button class="static_boxes" type="submit">${_("OK")}</button>
                    </td>
                </tr>
            </table>
        </div>

    </div>
</form>

</div>
</%def>
