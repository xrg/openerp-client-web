<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
<title>${_("Workflow")}</title>
 <!--meta content="text/html; charset=ISO-8859-1" http-equiv="content-type"-->
    <title></title>  
    <style>
        body, html {
            padding: 5px;
        }
    </style>    
</%def>

<%def name="content()">
    <table class="view" border="0">
        <tr>
            <td colspan="2">
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="100%"><h1>${_('Workflow (%s)') % name}</h1></td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <input type="hidden" id="workitems" name="workitems" value="${workitems}"/>
                ${form.display()}
            </td>
        </tr>
    </table>
</%def>
