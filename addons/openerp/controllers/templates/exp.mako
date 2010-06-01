<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>Export Data</title>
    <link href="/openerp/static/css/listgrid.css" rel="stylesheet" type="text/css"/>
    <script type="text/javascript" src="/openerp/static/javascript/listgrid.js"></script>

    <style type="text/css">
        .fields-selector {
            width: 100%;
            height: 400px;
        }

        .fields-selector-left {
            width: 45%;
        }
        
        td.fields-selector-left div#export_fields_left {
        	overflow: scroll;
        	width: 100%; 
        	height: 100%; 
        	border: solid #999999 1px;
        }

        .fields-selector-center {
            width: 15%;
        }

        .fields-selector-right {
            width: 45%;
        }

        .fields-selector select {
            width: 100%;
            height: 100%;
        }

        .fields-selector button {
            width: 100%;
            margin: 5px 0px;
        }
    </style>

    <script type="text/javascript">
        function add_fields(){
        
            var tree = ${tree.name};
            
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
            form.action = openobject.http.getURL('/openerp/impex/save_exp');
            
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
            model = openobject.dom.get('_terp_model').value;
            params = {'_terp_id': id, '_terp_model': model}
            
            req = openobject.http.postJSON('/openerp/impex/get_namelist', params);
            
            req.addCallback(function(obj){
                if (obj.error){
                    alert(obj.error);
                } else {
                    self.reload(obj.name_list);
                }
            });
        }
        
        function delete_listname(form) {
        
            var list = new ListView('_terp_list');
            var boxes = list.getSelectedItems();
                        
            if (boxes.length == 0){
                alert(_('Please select an item...'));
                return;
            }
            
            var id = boxes[0].value;
    
            params = {'_terp_id' : id};

            setNodeAttribute(form, 'action', openobject.http.getURL('/openerp/impex/delete_listname', params));
            form.submit();
        }
        
        function reload(name_list) {
            var select = openobject.dom.get('fields');

            forEach(name_list, function(f){                
                var text = f[1];
                var id = f[0]
                select.options.add(new Option(text, id));
            });
        }

        function do_export(form){

            var options = openobject.dom.get('fields').options;

            if (options.length == 0){
                return alert(_('Please select fields to export...'));
            }

            var fields2 = [];

            forEach(options, function(o){
                o.selected = true;
                fields2 = fields2.concat('"' + o.text + '"');
            });

            openobject.dom.get('_terp_fields2').value = '[' + fields2.join(',') + ']';

            setNodeAttribute(form, 'action', openobject.http.getURL('/openerp/impex/export_data/data.' + openobject.dom.get('export_as').value));
            form.submit();
        }
    </script>
</%def>

<%def name="content()">
    <form id='view_form' action="/openerp/impex/export_data" method="post" onsubmit="return false;">

    <input type="hidden" id="_terp_model" name="_terp_model" value="${model}"/>
    <input type="hidden" id="_terp_ids" name="_terp_ids" value="${ids}"/>
    <input type="hidden" id="_terp_search_domain" name="_terp_search_domain" value="${search_domain}"/>
    <input type="hidden" id="_terp_fields2" name="_terp_fields2" value="[]"/>

    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/openerp/static/images/stock/gtk-go-up.png"/>
                        </td>
                        <td width="100%">${_("Export Data")}</td>
                    </tr>
                </table>
            </td>
        </tr>        
        % if new_list.ids:
        <tr>
            <td>
                <div id='exported_list' style="overflow: auto;">${new_list.display()}</div>
            </td>
        </tr>
        <tr>
            <td class="toolbar">
            	<a class="button-a" href="javascript: void(0)" onclick="delete_listname(form);">${_("Delete")}</a>
            </td>
        </tr>
        % endif
        <tr>
            <td>
                <table class="fields-selector" cellspacing="5" border="0">
                    <tr>
                        <th class="fields-selector-left">${_("All fields")}</th>
                        <th class="fields-selector-center">&nbsp;</th>
                        <th class="fields-selector-right">${_("Fields to export")}</th>
                    </tr>
                    <tr>
                        <td class="fields-selector-left" height="400px">
                            <div id="export_fields_left">${tree.display()}</div>
                        </td>
                        <td class="fields-selector-center">
                        	<table border="0" cellpadding="0" cellspacing="0" width="100%">
                        		<tr>
                        			<td>
                        				<a class="button-a" href="javascript: void(0)" onclick="add_fields()">${_("Add")}</a>
                        			</td>
                        		</tr>
                        		<tr>
                        			<td>
                        				<a class="button-a" href="javascript: void(0)" onclick="del_fields()">${_("Remove")}</a>
                        			</td>
                        		</tr>
                        		<tr>
                        			<td>
                        				<a class="button-a" href="javascript: void(0)" onclick="del_fields(true)">${_("Nothing")}</a>
                        			</td>
                        		</tr>
                        		<tr>
                        			<td>
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
            <td>            
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
            <td>
                <fieldset>
                    <legend>${_("Options")}</legend>
                    <table>
                        <tr>
                            <td>
                                <select id="export_as" name="export_as">
                                    <option value="csv">${_("Export as CSV")}</option>
                                    <option value="xls">${_("Export as Excel")}</option>
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
        	<td>
        		<fieldset>
                    <legend>${_("Select an Option to Export")}</legend>
                    <table>
                        <tr>
                            <td>
                                <input type="checkbox" class="checkbox" name="import_compat" checked="checked"/>
                            </td>
                            <td>${_("Import Compatible")}</td>
                        </tr>
                    </table>
                </fieldset>
        	</td>
        </tr>
        <tr>
            <td>
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td width="100%">&nbsp;</td>
                            <td><a class="button-a" href="javascript: void(0)" onclick="do_export(form)">${_("Export")}</a></td>
                            <td><a class="button-a" href="javascript: void(0)" onclick="window.close()">${_("Close")}</a></td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</form>
</%def>
