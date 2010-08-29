<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${_("Module Management")}</title>
    <script type="text/javascript">
        var do_select = function(){}
    </script>
</%def>

<%def name="content()">

    <table class="view" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
            <td valign="top">
                <table width="100%" class="titlebar">
                    <tr>
                        <td nowrap="nowrap"><h1>${_("Web Modules")}</h1></td>
                     <tr>
                 </table>
             </td>
         </tr>
         <tr>
             <td valign="top">
                 ${form.screen.display()}
             </td>
         </tr>
    </table>
     
</%def>

