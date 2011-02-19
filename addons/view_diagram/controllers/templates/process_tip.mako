<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>
<%! show_header_footer = False %>

<%def name="header()">
    <title>${_("Process")}</title>
</%def>

<%def name="content()">
<table class="view" cellspacing="5" border="0" width="100%">
    <tr>
        <td>
            <div class="box2">
                ${title_tip}
            </div>
        </td>
    </tr>
    <tr>
        <td align="right">
            <div class="box2">
                <button type="button" onclick="window.top.closeAction()">${_("Close")}</button>
            </div>
        </td>
    </tr>
</table>

</%def>
