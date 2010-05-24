<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>View Editor</title>
    <script type="text/javascript" src="/openerp/static/javascript/form.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/m2o.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/viewed.js"></script>    
    <script type="text/javascript" src="/openerp/static/javascript/modalbox.js"></script>

    <link href="/openerp/static/css/modalbox.css" rel="stylesheet" type="text/css"/>
    <link href="/openerp/static/css/autocomplete.css" rel="stylesheet" type="text/css"/>
</%def>

<%def name="content()">
    <table class="view" border="0">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img alt="" src="/openerp/static/images/stock/gtk-edit.png"/>
                        </td>
                        <td width="100%">${_("View Editor %s - %s") % (view_id, model)}</td>
                    </tr>
                </table>
                <input type="hidden" id="view_model" value="${model}"/>
                <input type="hidden" id="view_id" value="${view_id}"/>
                <input type="hidden" id="view_type" value="${view_type}"/>
            </td>
        </tr>
        <tr>
            <td id="view_tr" height="500" width="auto">
                <div style="overflow-x: auto; overflow-y: scroll; width: 100%; height: 100%; border: solid #999999 1px;">${tree.display()}</div>
            </td>
        </tr>
        <tr class="toolbar">
            <td align="right">
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td>
                            	<a class="button-a" href="javascript: void(0)" title="${_('Create a new inherited view')}" onclick="onInherit('${model}')">${_("Inherited View")}</a>
                           	</td>
                            <td width="100%">&nbsp;</td>
                            <td>
                            	<a class="button-a" href="javascript: void(0)" onclick="onPreview()">${_("Preview")}</a>
                           	</td>
                            <td>
                            	<a class="button-a" href="javascript: void(0)" onclick="onClose()">${_("Close")}</a>
                           	</td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</%def>
