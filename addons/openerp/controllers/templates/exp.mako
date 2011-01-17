<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>Export Data</title>

    <link rel="stylesheet" type="text/css" href="/openerp/static/css/impex.css"/>

    <script type="text/javascript">
        function add_fields(){

            var tree = treeGrids['${tree.name}'];

            var fields = tree.selection;

            var select = openobject.dom.get('fields');

            var opts = {};
            forEach(select.options, function(o){
                opts[o.value] = o;
            });

            forEach(fields, function(f){

                var text = f.record.items.name;

                var id = f.record.id;

                if (id in opts) return;

                select.options.add(new Option(text, id));
            });

        }

        function save_fields() {
            var $savelist = jQuery('#savelist');
            $savelist.toggle();
            if($savelist.is(':hidden')) { return; }
            $savelist.find('input').focus();
        }

        function save_export() {
            var form = document.forms['view_form'];
            form.action = '/openerp/impex/save_exp';
            var options = openobject.dom.get('fields').options;
            forEach(options, function(o){
                o.selected = true;
            });
            form.submit();
        }

        function del_fields(all){

            var fields = filter(function(o){return o.selected;}, openobject.dom.get('fields').options);

            if (all){
                openobject.dom.get('fields').innerHTML = '';
            } else {
                forEach(fields, function(f){
                    removeElement(f);
                });
            }
        }

        function do_select() {
            var id = jQuery('#saved_fields').val();
            if(!id) { reload([]); return; }

            var req = jQuery.get('/openerp/impex/namelist', {
                '_terp_id': id,
                '_terp_model': jQuery('#_terp_model').val()
            }, function(obj){
                if (obj.error){
                    error_display(obj.error);
                } else {
                    reload(obj.name_list);
                }
            }, 'json');
        }

        function do_import_cmp(){
            jQuery('#view_form').attr({
                'action': openobject.http.getURL('/openerp/impex/exp', {
                    'import_compat': jQuery('#import_compat').val()
                })
            }).submit();
        }

        function delete_listname() {
            var form = document.forms['view_form'];

            var id = jQuery('#saved_fields').val();
            if(!id) { return; }
            form.action = openobject.http.getURL('/openerp/impex/delete_listname', {'_terp_id' : id});
            form.submit();
        }

        function reload(name_list) {
            var $fields_list = jQuery('#fields');
            $fields_list.empty();
            jQuery.each(name_list, function (_, f) {
                $fields_list.append(new Option(f[1], f[0]));
            });
        }

        function do_export(form){

            var options = openobject.dom.get('fields').options;

            if (options.length == 0){
                error_display(_('Please select fields to export...'));
                return;
            }

            var fields2 = [];

            forEach(options, function(o){
                o.selected = true;
                fields2 = fields2.concat('"' + o.text + '"');
            });
            openobject.dom.get('_terp_fields2').value = '[' + fields2.join(',') + ']';
            jQuery(idSelector(form)).attr('action', openobject.http.getURL(
                '/openerp/impex/export_data/data.csv')
            ).submit();
        }

        jQuery(document).ready(function () {
            // Set the page's title as title of the dialog
            var $header = jQuery('.pop_head_font');
            window.frameElement.set_title(
                $header.text());
            $header.closest('.side_spacing').parent().remove();
        });
    </script>
</%def>

<%def name="content()">
    <form id='view_form' action="/openerp/impex/export_data" method="post" target="_self" onsubmit="return false;">

    <input type="hidden" id="_terp_model" name="_terp_model" value="${model}"/>
    <input type="hidden" id="_terp_ids" name="_terp_ids" value="${ids}"/>
    <input type="hidden" id="_terp_search_domain" name="_terp_search_domain" value="${search_domain}"/>
    <input type="hidden" id="_terp_fields2" name="_terp_fields2" value="[]"/>
    <input type="hidden" id="_terp_context" name="_terp_context" value="${ctx}"/>

    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td class="side_spacing">
                <table width="100%" class="popup_header">
                    <tr>
                        <td align="center" class="pop_head_font">${_("Export Data")}</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td class="side_spacing" align="left">
                This wizard will export all data that matches the current search criteria to a CSV file.
                You can export all data or only the fields that can be reimported after modification.
            </td>
        </tr>
        <tr>
            <td class="side_spacing">
                <table>
                    <tr>
                        <td class="label"><label for="import_compat">${_("Export Type:")}</label></td>
                        <td>
                            <select id="import_compat" name="import_compat" onchange="do_import_cmp();">
                                <option value="1">${_("Import Compatible Export")}</option>
                                <option value="0"
                                    ${'selected=selected' if import_compat == "0" else ''}
                                    >${_("Export all Data")}</option>
                            </select>
                        </td>
                    </tr>
                </table>
            </td>
        </tr> 
        <tr>
            <td class="side_spacing">
                <table class="fields-selector-export" cellspacing="5" border="0">
                    <tr>
                        <th class="fields-selector-left">${_("Available fields")}</th>
                        <th class="fields-selector-center">&nbsp;</th>
                        <th class="fields-selector-right">${_("Fields to export")}
                            <a style="color: blue;" href="#"
                               onclick="save_fields(); return false;">${_("Save fields list")}</a>
                            <div id="savelist" style="display:none;">
                                <label for="savelist_name">${_("Save as:")}</label>
                                <input type="text" id="savelist_name" name="savelist_name"/>
                                <a class="button-a" href="javascript: void(0)" onclick="save_export()">${_("OK")}</a>
                            </div>
                            % if existing_exports:
                            <div>
                                <label for="saved_fields">${_("Saved exports:")}</label><br>
                                <select id="saved_fields" name="saved_exports" onchange="do_select();"
                                        style="width: 60%;">
                                    <option></option>
                                    % for export in existing_exports:
                                        <option value="${export['id']}">${export['name']}</option>
                                    % endfor
                                </select>
                                <a class="button-a" href="#" onclick="delete_listname(); return false;"
                                        >${_("Delete")}</a>
                            </div>
                            % endif
                        </th>
                    </tr>
                    <tr>
                        <td class="fields-selector-left" height="400px">
                            <div id="fields_left">${tree.display()}</div>
                        </td>
                        <td class="fields-selector-center">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td align="center">
                                        <a class="button-a" href="javascript: void(0)" onclick="add_fields()">${_("Add")}</a>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center">
                                        <a class="button-a" href="javascript: void(0)" onclick="del_fields()">${_("Remove")}</a>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center">
                                        <a class="button-a" href="javascript: void(0)" onclick="del_fields(true)">${_("Remove All")}</a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                        <td class="fields-selector-right" height="400px">
                            <select name="fields" id="fields" multiple="multiple"></select>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td class="side_spacing">
                <table width="100%">
                    <tr>
                        <td class="imp-header" align="right">
                            <a class="button-a" href="javascript: void(0)" onclick="window.frameElement.close()">${_("Cancel")}</a>
                            <a class="button-a" href="javascript: void(0)" onclick="do_export('view_form')">${_("Export to File")}</a>
                        </td>
                        <td width="5%"></td>
                </table>
            </td>
        </tr>
    </table>
</form>
</%def>
