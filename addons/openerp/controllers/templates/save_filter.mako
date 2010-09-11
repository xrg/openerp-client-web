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
</%def>

<%def name="content()">
    <form id="filter_sc" name="filter_sc" method="POST" action="/openerp/search/do_filter_sc">
        <input type="hidden" id="model" name="model" value="${model}"/>
        <input type="hidden" id="domain" name="domain" value="${domain}"/>
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
                                <button type="submit">${_("Save")}</button>
                                <button type="reset">${_("Close")}</button>
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
                                <td class="label" style="padding: 0;">
                                    <label for="sc_name">${_("Filter Name")}:</label>
                                </td>
                                <td width="100%">
                                    <input type="text" name="name" id="sc_name" style="width: 100%;"/>
                                </td>
                            </tr>
                        </table>
                    </div>
                </td>
            </tr>
        </table>
    </form>
    <script type="text/javascript">
        jQuery('#filter_sc').
                bind('reset', function () { jQuery.fancybox.close(); }).
                submit(function () {
                    var $this = jQuery(this);
                    $this.ajaxSubmit({
                        dataType:'json',
                        success:  function(obj) {
                            if(obj.filter) {
                                jQuery('#filter_list').
                                    append(jQuery("<option>", {
                                        value: obj.filter[0],
                                        group_by: obj.filter[2]
                                    }).text(obj.filter[1]));
                                jQuery.fancybox.close();
                            }
                        }
                    });
                    return false;
                });
    </script>
</%def>
