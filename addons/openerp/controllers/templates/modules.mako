<%inherit file="/openerp/controllers/templates/xhr.mako"/>

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
                        <td width="32px" align="center">
                            <img alt="" src="/openerp/static/images/stock/gtk-find.png"/>
                        </td>
                        <td nowrap="nowrap">Web Modules</td>
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

