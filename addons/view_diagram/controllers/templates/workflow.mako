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
                        <td width="32px" align="center">
                            <img src="/openerp/static/images/stock/gtk-refresh.png"/>
                        </td>
                        <td width="100%">${_('Workflow (%s)') % name}</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <table width="100%">
                    <tr>                        
                        <td>
                            <input type="hidden" id="workitems" name="workitems" value="${workitems}"/>
                            ${form.display()}
                        </td>                        
                    </tr>
                </table>
            </td>
        </tr>
        <tr class="toolbar">
            <td align="right" colspan="2">
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td align="left" id="status" style="width: 100%; ">&nbsp;</td>
                            <td><button type="button" onclick="window.close()">${_("Close")}</button></td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</%def>
