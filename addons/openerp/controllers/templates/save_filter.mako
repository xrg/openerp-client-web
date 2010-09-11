<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>Save as a Shortcut</title>
    <style type="text/css">
        td.save_filter {
            padding: 10px 10px 0 10px;;
        }
        
        td.save_filter h1 {
            padding: 0 0 5px 0;
        }
    </style>
    <script type="text/javascript">

        var onFilterClose = function(form) {
            var args = {model: jQuery('#model').val(),
                        domain: jQuery('#domain').val(),
                        group_by: jQuery('#group_by').val(),
                        name: jQuery('#sc_name').val()
                        }
            jQuery.ajax({
                url: '/openerp/search/do_filter_sc',
                type: 'POST',
                dataType: 'json',
                data: args,
                success: function(obj) {
                    if(obj.filter) {
                        jQuery('#filter_list').
                            append(jQuery("<option></option>").
                            attr("value", obj.filter[0]).
                            attr("group_by", obj.filter[2]).
                            text(obj.filter[1]));
                        jQuery.fancybox.close();
                    }
                }
            });
        }

    </script>
</%def>

<%def name="content()">
    <form id="filter_sc" name="filter_sc" method="POST" action="return false;">
        <input type="hidden" id="model" name="model" value="${model}"/>
        <input type="hidden" id="domain" name="domain" value="${domain}"/>
        <input type="hidden" id="flag" name="flag" value="${flag}"/>
        <input type="hidden" id="group_by" name="group_by" value="${group_by}"/>
        <table class="view" width="100%" border="0">
            <tr>
                <td style="padding: 10px 10px 0 10px;">
                    <table width="100%" style="border: none;">
                        <tr>
                            <td class="save_filter">
                                <h1>${_("Save as a Filter")}</h1>
                            </td>
                        </tr>
                        <tr>
                            <td class="save-filter-header">
                                <a class="button-a" href="javascript: void(0)" onclick="onFilterClose('filter_sc');">${_("Save")}</a>
                                <a class="button-a" href="javascript: void(0)" onclick="jQuery.fancybox.close();">${_("Close")}</a>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr>
                <td style="padding: 10px 10px 0 10px;">
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
                </td>
            </tr>
        </table>
    </form>
</%def>
