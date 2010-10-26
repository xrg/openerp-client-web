<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>Save as Shortcut</title>
</%def>

<%def name="content()">
    <form id="filter_sc" name="filter_sc" method="POST" action="/openerp/search/do_filter_sc">
        <input type="hidden" id="model" name="model" value="${model}"/>
        <input type="hidden" id="domain" name="domain" value="${domain}"/>
        <input type="hidden" id="group_by" name="group_by" value="${group_by}"/>
        <table class="view" width="100%" border="0">
            <tr>
                <td style="padding: 0">
                    <table width="100%" style="border: none;">
                        <tr>
                            <td style="padding: 0 10px 5px 10px">
                                <h1>${_("Save as Filter")}</h1>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr>
                <td style="padding: 0 10px">
                    <div class="box2">
                        <table border="0" width="100%" align="center">
                            <tr>
                                <td class="label" style="padding: 0 4px 0 0;">
                                    <label for="sc_name">${_("Filter Name")}:</label>
                                </td>
                                <td width="100%">
                                    <input type="text" name="name" id="sc_name" value="${filtername}" style="width: 100%;" autofocus="true"/>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <table width="100%" style="border: none; margin-top: 10px">
                        <tr>
                            <td style="padding: 0 10px 3px 10px" align="right">
                                <button type="submit" id="save_submit">${_("Save")}</button>
                                <button type="reset">${_("Close")}</button>
                            </td>
                        </tr>
                    </table>
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
                            var $filterOptions = jQuery("#filter_list_options_group option");
                            if(!obj.new_id) {
                                $filterOptions.each(function() {
                                    if (jQuery(this).text().toLowerCase() == obj.filter[1].toLowerCase()){
                                        this.text = obj.filter[1];
                                        this.selected = this.text;
                                        this.value = obj.filter[0];
                                        this.group_by = obj.filter[2];
                                    }
                                });
                            }
                            else {
                                jQuery('#filter_list_options_group').
                                    append(jQuery("<option>", {
                                        selected: 'selected',
                                        value: obj.filter[0],
                                        group_by: obj.filter[2]
                                    }).text(obj.filter[1]));

                                var filters = jQuery("#filter_list_options_group option");
                                filters.sort(function(a,b) {
                                    var match1 = $(a).text().toUpperCase();
                                    var match2  = $(b).text().toUpperCase();
                                    return (match1 < match2) ? -1 : (match1 > match2) ? 1 : 0;
                                });
                                $('#filter_list_options_group').empty().append(filters);
                                $('#filter_list').data('previousIndex', $('#filter_list').attr('selectedIndex'));
                            }
                            jQuery.fancybox.close();
                        }
                    });
                    return false;
                });
    </script>
</%def>
