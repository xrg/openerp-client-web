<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>Export Data</title>
    <link href="/static/css/listgrid.css" rel="stylesheet" type="text/css"/>
    <script type="text/javascript" src="/static/javascript/listgrid.js"></script>

    <style type="text/css">
        .fields-selector {
            width: 100%;
            height: 400px;
        }

        .fields-selector-left {
            width: 45%;
        }

        .fields-selector-center {
            width: 10%;
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
        
            var tree = ${tree.field_id};
            
            var fields = tree.selection;
            var select = $('fields');

            var opts = {};
            forEach($('fields').options, function(o){
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
            var elem = $(id);
            elem.style.display = elem.style.display == 'none' ? '' : 'none';
        }

        function save_export() {
            var form = document.forms['view_form'];
            form.action = '/impex/save_exp';
            
            var options = $('fields').options;            
            forEach(options, function(o){
                o.selected = true;
            });
            
            form.submit();        
        }
        
        function del_fields(all){

            var fields = filter(function(o){return o.selected;}, $('fields').options);

            if (all){
                $('fields').innerHTML = '';
            } else {
                forEach(fields, function(f){
                    removeElement(f);
                });
            }
        }
        
        function do_select(id, src) {
            $('fields').innerHTML = '';
            model = $('_terp_model').value;
            params = {'_terp_id': id, '_terp_model': model}
            
            req = Ajax.JSON.post('/impex/get_namelist', params);
            
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
                alert('Please select a List name...');
                return;
            }
            
            var id = boxes[0].value;
    
            params = {'_terp_id' : id};

            setNodeAttribute(form, 'action', getURL('/impex/delete_listname', params));
            form.submit();
        }
        
        function reload(name_list) {
            var select = $('fields');

            forEach(name_list, function(f){                
                var text = f[1];
                var id = f[0]
                select.options.add(new Option(text, id));
            });
        }

        function do_export(form){

            var options = $('fields').options;

            if (options.length == 0){
                return alert('Please select fields to export...');
            }

            var fields2 = [];

            forEach(options, function(o){
                o.selected = true;
                fields2 = fields2.concat('"' + o.text + '"');
            });

            $('_terp_fields2').value = '[' + fields2.join(',') + ']';

            setNodeAttribute(form, 'action', '/impex/export_data/data.' + $('export_as').value);
            form.submit();
        }
    </script>
</head>
<body>

<form id='view_form' action="/impex/export_data" method="post">

    <input type="hidden" id="_terp_model" name="_terp_model" value="${model}"/>
    <input type="hidden" id="_terp_ids" name="_terp_ids" value="${ustr(ids)}"/>
    <input type="hidden" id="_terp_search_domain" name="_terp_search_domain" value="${ustr(search_domain)}"/>
    <input type="hidden" id="_terp_fields2" name="_terp_fields2" value="[]"/>

    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/static/images/stock/gtk-go-up.png"/>
                        </td>
                        <td width="100%">Export Data</td>
                    </tr>
                </table>
            </td>
        </tr>        
        <tr>
            <td>
                <div py:if="new_list.ids" id='exported_list' py:content="new_list.display()" style="height: 142px; overflow: auto;">                    
                </div>
            </td>
        </tr>
        <tr>
            <td py:if="new_list.ids" class="toolbar">
                <button type="button" onclick="delete_listname(form);">Delete</button>
            </td>
        </tr>
        <tr>
            <td>
                <table class="fields-selector" cellspacing="5" border="0">
                    <tr>
                        <th class="fields-selector-left">All fields</th>
                        <th class="fields-selector-center">&nbsp;</th>
                        <th class="fields-selector-right">Fields to export</th>
                    </tr>
                    <tr>
                        <td class="fields-selector-left" height="400px">
                            <div py:content="tree.display()" style="overflow: scroll; width: 100%; height: 100%; border: solid #999999 1px;"/>
                        </td>
                        <td class="fields-selector-center">
                            <button type="button" onclick="add_fields()">Add</button><br/>
                            <button type="button" onclick="del_fields()">Remove</button><br/>
                            <button type="button" onclick="del_fields(true)">Nothing</button><br/><br/>
                            <button type="button" onclick="open_savelist('savelist')">Save List</button>
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
                        <legend>Save List</legend>
                        <table>
                            <tr>                           
                                <td class="label">Name of This Export:</td>                            
                                <td>
                                    <input type="text" id="savelist_name" name="savelist_name"/>
                                </td>
                                <td>
                                    <button type="button" onclick="save_export()">OK</button>
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
                    <legend>Options</legend>
                    <table>
                        <tr>
                            <td>
                                <select id="export_as" name="export_as">
                                    <option value="csv">Export as CSV</option>
                                    <option value="xls">Export as Excel</option>
                                </select>
                            </td>
                            <td>
                                <input type="checkbox" class="checkbox" name="add_names" checked="checked"/>
                            </td>
                            <td>Add field names</td>
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
                            <td><button type="button" onclick="do_export(form)">Export</button></td>
                            <td><button type="button" onclick="window.close()">Close</button></td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</form>

</body>
</html>
