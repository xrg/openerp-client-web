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
                        <tr>
                            <td style="padding: 0 10px 3px 10px">
                                <button type="submit">${_("Save")}</button>
                                <button type="reset">${_("Close")}</button>
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
                                <td class="label" style="padding: 0;">
                                    <label for="sc_name">${_("Filter Name")}:</label>
                                </td>
                                <td width="100%">
                                    <input type="text" name="name" id="sc_name" value="${filtername}" style="width: 100%;"/>
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
                            var in_filter = false;
                            jQuery("#filter_list option").each(function() {
                                if (obj.filter && this.text == obj.filter[1]){
                                    this.selected = this.text;
                                    this.value = obj.filter[0];
                                    this.group_by = obj.filter[2];
                                    in_filter = true;
                                }
                            });

                            if(obj.filter && !in_filter) {
                                jQuery('#filter_list').
                                    append(jQuery("<option>", {
                                        selected: 'selected',
                                        value: obj.filter[0],
                                        group_by: obj.filter[2]
                                    }).text(obj.filter[1]));
                            }
                            jQuery.fancybox.close();
                        }
                    });
                    return false;
                });
    </script>
</%def>
