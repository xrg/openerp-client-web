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

            var prefix = ${tree.field_id}.id + '_row_';
            var fields = ${tree.field_id}.selection;

            var select = $('fields');

            var opts = {};
            forEach($('fields').options, function(o){                
                opts[o.value] = o;
            });

            forEach(fields, function(f){

                var text = f.getElementsByTagName('a')[0].innerHTML;
                var id = f.id.replace(prefix, '');

                if (id in opts) return;
                               
                select.options.add(new Option(text, id));
            });
        }

        function open_savelist(id) {
            if($(id).style.display == 'none') {
                $(id).style.display = '';
            }
            else {
                $(id).style.display = 'none';
            }
        }
        
        function save_name(textbox_id) {
        
            name = document.getElementById(textbox_id).value;
            model = $('_terp_model').value;
            fields = $('fields');
            var ids = [];
            var val = [];
        
            if(!document.getElementById(textbox_id).value)
                return;
            else {
                forEach(fields, function(e){
                    val = val.concat("'"+ e.innerHTML + "'");                    
                    ids = ids.concat("'"+ e.value + "'");
                });
            }
            
            val = '[' + val.join(',') + ']';
            
            if(ids.length &lt; 1)
                return;

            ids = '[' + ids.join(',') + ']';

            var params = {'_terp_model': model, '_terp_ids': ids, '_terp_name': name, '_terp_val': val};
            var req = Ajax.JSON.post('/impex/save_list', params);
            
            req.addCallback(function(obj){
                if (obj.error){
                    alert(obj.error);
                } else {
                    self.reload();
                }
            });
        }
        
        function reload() {
        
            id = $('exported_list');
            model = $('_terp_model').value;
            
            var params = {'_terp_model': model};
            var req = Ajax.JSON.post('/impex/reload_predef_list', params);
            
            req.addCallback(function(obj){               
                                               
                var th1 = TH({style: "text-align: left;"}, 'Export Name');
                var th2 = TH({style: "text-align: left;"}, 'Exported Fields');
                
                var tr = TR(null, th1);
                appendChildNodes(tr, th2);
                
                var trs = map(function(x){return TR(null, TD(null, x[1]), TD(null, x[2]))}, obj.predef_list);
                
              
                var table = TABLE({'width': '100%', 'border' : '1'}, TBODY(null, tr, trs));
                
                var div = DIV({id: 'exported_list', style: "height: 150px; overflow: auto;"}, table);
                
                swapDOM(id, div);                
            });                       
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

            var pwin = window.opener;
            var src = pwin.document.getElementById('${source}');

            var ids = new ListView(src).getSelectedRecords();
            var id = '[]';

            $('_terp_ids').value = '[' + ids.join(',') + ']';
            $('_terp_fields2').value = '[' + fields2.join(',') + ']';

            setNodeAttribute(form, 'action', '/impex/export_data/data.' + $('export_as').value);
            form.submit();
        }
    </script>
</head>
<body>

<form action="/impex/export_data" method="post">

    <input type="hidden" id="_terp_model" name="_terp_model" value="${model}"/>
    <input type="hidden" id="_terp_ids" name="_terp_ids" value="[]"/>
    <input type="hidden" id="_terp_search_domain" name="_terp_search_domain" value="${ustr(search_domain)}"/>
    <input type="hidden" id="_terp_fields2" name="_terp_fields2" value="[]"/>

    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/static/images/icon.gif"/>
                        </td>
                        <td width="100%">Export Data</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <div id='exported_list' style="height: 150px; overflow: auto;">
                    <table border='1' width="100%">
                        <tr>
                            <th class="label" style="text-align: left;">
                                Export Name
                            </th>
                            <th class="label" style="text-align: left;">
                                Exported Fields
                            </th>
                        </tr>
                        <tr py:for="nm in predef_list">                        
                            <td>                      
                               ${nm[1]}
                            </td>
                            <td>
                                ${nm[2]}
                            </td>                                                               
                        </tr>                                         
                    </table>
                </div>           
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
                            <td class="label">
                                Name of This Export :    
                            </td>                            
                            <td>
                                <input type="text" id="savelist_name" name="savelist_name"/>
                            </td>
                            <td>
                                <button type="button" onclick="save_name('savelist_name')">Ok</button>
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
