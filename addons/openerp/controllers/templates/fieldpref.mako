<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${_("Field Preferences")}</title>
    
    <script type="text/javascript">
        jQuery(document).ready(function(){
            if(openobject.dom.get('click_ok').value)
                window.close();
        });
    </script>
</%def>

<%def name="content()">
<form action="/openerp/fieldpref/save" method="post">

    <input id="_terp_model" name="_terp_model" value="${model}" type="hidden"/>
    <input id="_terp_model" name="_terp_field/name" value="${field['name']}" type="hidden"/>
    <input id="_terp_model" name="_terp_field/value" value="${field['value']}" type="hidden"/>
    <input id="_terp_model" name="_terp_field/string" value="${field['string']}" type="hidden"/>
    <input id="_terp_model" name="_terp_deps2" value="${deps}" type="hidden"/>
    <input id="click_ok" name="click_ok" value="${click_ok}" type="hidden"/>

    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="100%"><h1>${_("Field Preferences")}</h1></td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <div class="box2">
                    <table border="0" width="100%" align="center">
                        <tr>
                            <td class="label">${_("Field Name:")}</td>
                            <td class="item" width="100%"><input type="text" disabled="disabled" value="${field['string']}"/></td>
                        </tr>
                        <tr>
                            <td class="label">${_("Domain:")}</td>
                            <td class="item"><input type="text" disabled="disabled" value="${model}"/></td>
                        </tr>
                        <tr>
                            <td class="label">${_("Default Value:")}</td>
                            <td class="item"><input type="text" disabled="disabled" value="${field['value']}"/></td>
                        </tr>
                    </table>
                </div>
                <div class="box2">
                    <table border="0" width="100%">
                        <tr>
                            <td colspan="2">
                                <fieldset>
                                    <legend><strong>${_("Value applicable for:")}</strong></legend>
                                    <table border="0">
                                        <tr>
                                            <td class="item">
                                                <input type="radio" class="radio" name="_terp_you" value="True" checked="checked"/>
                                            </td>
                                            <td>${_("Only for you")}</td>
                                            <td class="item">
                                                <input type="radio" class="radio" name="_terp_you" value="False"/>
                                            </td>
                                            <td>${_("For all")}</td>
                                        </tr>
                                    </table>
                                </fieldset>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2">
                                <fieldset>
                                    <legend><strong>${_("Value applicable if:")}</strong></legend>
                                    <table border="0">
                                        % if not deps:
                                        <tr><td align="center">${_("Always applicable!")}</td></tr>
                                        % else:
                                        <tr>
                                            % for n, n, v, v in deps:
                                                <td><input type="checkbox" class="checkbox" name="_terp_deps/${n}" value="${v}"/></td><td>${n} = ${v}</td>
                                            % endfor
                                        </tr>
                                        % endif
                                    </table>
                                </fieldset>
                            </td>
                        </tr>
                    </table>
                </div>
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td width="100%">
                            </td>
                            <td>
                            	<a class="button-a" href="javascript: void(0)" onclick="window.close()">${_("Close")}</a>
                            </td>
                            <td>
                                <button type="submit">${_("OK")}</button>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</form>
</%def>
