<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>Save as a Shortcut</title>

    <script type="text/javascript">

        var onFilterClose = function(form) {
            jQuery('#'+form).submit();
            // window.opener.document.getElementById('filter_list').selectedIndex = 0;
            window.close();
            window.opener.location.reload();
        }

    </script>
</%def>

<%def name="content()">
    <form id="filter_sc" name="filter_sc" method="POST" action="/openerp/search/do_filter_sc">
        <input type="hidden" id="model" name="model" value="${model}"/>
        <input type="hidden" id="domain" name="domain" value="${domain}"/>
        <input type="hidden" id="flag" name="flag" value="${flag}"/>
        <input type="hidden" id="group_by" name="group_by" value="${group_by}"/>
        <table class="view" width="100%" border="0">
            <tr>
                <td align="center" style="padding: 20px 0 0 0;">
                    <table>
                        <tr>
                            <td class="popup_header" style="padding: 0px; width: 470px;">${_("Save as a Filter")}</td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr>
                <td style="padding: 0px;">
                    <div class="box2">
                        <table border="0" width="100%" align="center">
                            <tr>
                                <td class="label" style="padding: 0px;">
                                    <label for="sc_name">${_("Filter Name")}:</label>
                                </td>
                                <td width="100%">
                                    <input type="text" name="sc_name" id="sc_name" style="width: 100%;"/>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <div class="toolbar" align="center">
                        <table border="0" cellpadding="0" cellspacing="0" style="width: 470px;" class="popup_footer">
                            <tr>
                                <td width="100%" style="padding: 0 4px 0 0;">
                                    <a class="button-a" style="float: right;"" href="javascript: void(0)" onclick="onFilterClose('filter_sc');">${_("Save")}</a>
                                </td>
                                <td style="padding: 0 10px 0 0;">
                                    <a class="button-a" href="javascript: void(0)" onclick="window.close();">${_("Close")}</a>
                                </td>
                            </tr>
                        </table>
                    </div>
                </td>
            </tr>
        </table>
    </form>
</%def>
