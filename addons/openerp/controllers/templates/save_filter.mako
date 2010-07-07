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
                <td align="center" style="padding: 10px 0 0 0;">
                    <table>
                        <tr>
                            <td class="view_log_header" style="padding: 0px;">${_("Save as a Filter")}</td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr>
                <td style="padding: 0px;">
                    <div class="box2">
                        <table border="0" width="100%" align="center">
                            <tr>
                                <td class="label" width="50%">
                                    <label for="sc_name">${_("Filter Name")}:</label>
                                </td>
                                <td width="50%">
                                    <input type="text" name="sc_name" id="sc_name"/>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <div class="toolbar" align="center">
                        <table border="0" cellpadding="0" cellspacing="0" class="save_filter_footer">
                            <tr>
                                <td width="90%" align="right">
                                    <a class="button-a" href="javascript: void(0)" onclick="window.close()" style="float: none;">${_("Close")}</a>
                                </td>
                                <td>
                                    <a class="button-a" href="javascript: void(0)" onclick="onFilterClose('filter_sc');">${_("Save")}</a>
                                </td>
                            </tr>
                        </table>
                    </div>
                </td>
            </tr>
        </table>
    </form>
</%def>
