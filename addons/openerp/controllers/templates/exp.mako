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
            forEach(openobject.dom.get('fields').options, function(o){
                opts[o.value] = o;
            });

            forEach(fields, function(f){

                var text = f.record.items.name;
                var id = f.record.id;

                if (id in opts) return;

                select.options.add(new Option(text, id));
            });
        }

        function open_savelist(id) {
            var elem = openobject.dom.get(id);
            elem.style.display = elem.style.display == 'none' ? '' : 'none';
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

        function do_select(id, src) {
            openobject.dom.get('fields').innerHTML = '';
            var model = openobject.dom.get('_terp_model').value;
            var req = openobject.http.postJSON('/openerp/impex/get_namelist', {
                '_terp_id': id,
                '_terp_model': model
            });

            req.addCallback(function(obj){
                if (obj.error){
                    error_display(obj.error);
                } else {
                    self.reload(obj.name_list);
                }
            });
        }

        function delete_listname() {
			var form = document.forms['view_form'];
            var list = new ListView('_terp_list');
            var boxes = list.getSelectedItems();

            if (boxes.length == 0){
                error_display(_('Please select an item...'));
                return;
            }

            var id = boxes[0].value;
            form.action = openobject.http.getURL('/openerp/impex/delete_listname', {'_terp_id' : id});
  			form.submit();

        }

        function reload(name_list) {
            var select = openobject.dom.get('fields');

            forEach(name_list, function(f){
                var text = f[1];
                var id = f[0];
                select.options.add(new Option(text, id));
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
            jQuery('#'+form).attr('target', 'new');
            jQuery('#'+form).attr('action', openobject.http.getURL(
                '/openerp/impex/export_data/data.' + openobject.dom.get('export_as').value)
            ).submit();
        }
    </script>
</%def>

<%def name="content()">
    <form id='view_form' action="/openerp/impex/export_data" method="post" onsubmit="return false;">

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
                    	<td class="exp-header" align="left">
                    		<a class="button-a" href="javascript: void(0)" onclick="do_export('view_form')">${_("Export")}</a>
                            <a class="button-a" href="javascript: void(0)" onclick="window.close()">${_("Close")}</a>
                    	</td>
                        <td align="center" class="pop_head_font">${_("Export Data")}</td>
                        <td width="30%"></td>
                    </tr>
                </table>
            </td>
        </tr>
        % if new_list.ids:
        <tr>
            <td class="side_spacing">
                <div id='exported_list'>${new_list.display()}</div>
            </td>
        </tr>
        <tr>
            <td class="side_spacing">
            	<table class="popup_header" width="100%">
            		<tr>
            			<td class="exp-header">
            				<a class="button-a" href="javascript: void(0)" onclick="delete_listname();">${_("Delete")}</a>
            			</td>
            		</tr>
            	</table>
            </td>
        </tr>
        % endif
        <tr>
            <td class="side_spacing">
                <table class="fields-selector-export" cellspacing="5" border="0">
                    <tr>
                        <th class="fields-selector-left">${_("All fields")}</th>
                        <th class="fields-selector-center">&nbsp;</th>
                        <th class="fields-selector-right">${_("Fields to export")}</th>
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
                        				<a class="button-a" href="javascript: void(0)" onclick="del_fields(true)">${_("Nothing")}</a>
                        			</td>
                        		</tr>
                        		<tr>
                        			<td align="center">
                        				<a class="button-a" href="javascript: void(0)" onclick="open_savelist('savelist')">${_("Save List")}</a>
                        			</td>
                        		</tr>
                        	</table>
                        </td>
                        <td class="fields-selector-right" height="400px">
                            <select name="fields" id="fields" multiple="multiple"/>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td class="side_spacing">
                <div id="savelist" style="display: none">
                    <fieldset>
                        <legend>${_("Save List")}</legend>
                        <table>
                            <tr>
                                <td class="label">${_("Name of This Export:")}</td>
                                <td>
                                    <input type="text" id="savelist_name" name="savelist_name"/>
                                </td>
                                <td>
                                	<a class="button-a" href="javascript: void(0)" onclick="save_export()">${_("OK")}</a>
                                </td>
                            </tr>
                        </table>
                    </fieldset>
                </div>
            </td>
        </tr>
        <tr>
            <td class="side_spacing">
                <fieldset>
                    <legend>${_("Options")}</legend>
                    <table>
                        <tr>
                            <td>
                                <select id="export_as" name="export_as">
                                    % for (k, v) in options:
							            <option value="${k}" selected="1">${v}</option>
            						% endfor
                                </select>
                            </td>
                            <td>
                                <input type="checkbox" class="checkbox" name="add_names" checked="checked"/>
                            </td>
                            <td>${_("Add field names")}</td>
                        </tr>
                    </table>
                </fieldset>
            </td>
        </tr>
        <tr>
        	<td class="side_spacing">
        		<fieldset title="Restricts the number of exportable fields to ensure you will be able to import your data back in OpenERP">
                    <legend>${_("Select an Option to Export")}</legend>
                    <table>
                        <tr>
                            <td>
                                <input type="checkbox" class="checkbox" name="import_compat" id="import_compat"/>
                            </td>
                            <td><label for="import_compat"
                                    >${_("Import Compatible")}</label></td>
                        </tr>
                    </table>
                </fieldset>
        	</td>
        </tr>
    </table>
</form>
</%def>
