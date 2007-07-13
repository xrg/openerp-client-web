<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">
<head>
    <title>Export Data</title>    
    <link href="/static/css/listgrid.css" rel="stylesheet" type="text/css"/>        
    <script type="text/javascript" src="/static/javascript/listgrid.js"></script>
    
    <style type="text/css">
        .fields-selector {
            width: 100%;
            height: 450px;
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
        
        .fields-selector td {
            height: 100%;
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
            
            var opts = {};
            forEach($('fields').options, function(o){
                opts[o.id] = o;
            });
            
            forEach(fields, function(f){
                var text = f.getElementsByTagName('a')[0].innerHTML;
                var id = f.id.replace(prefix, ''); 
                
                if (id in opts) return;
                
                var o = OPTION({id: id}, text);
                
                appendChildNodes('fields', o);                                
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
        
    </script>    
</head>
<body>
    
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
                <table class="fields-selector" cellspacing="5" border="0">
                    <tr>
                        <th class="fields-selector-left">All fields</th>
                        <th class="fields-selector-center">&nbsp;</th>
                        <th class="fields-selector-right">Fields to export</th>
                    </tr>
                    <tr>
                        <td class="fields-selector-left">
                            <div py:content="tree.display()" style="overflow: auto; width: 100%; height: 100%; border: solid lightgray 1px;"/>
                        </td>
                        <td class="fields-selector-center">
                            <button type="button" onclick="add_fields()">Add</button>
                            <button type="button" onclick="del_fields()">Remove</button>
                            <button type="button" onclick="del_fields(true)">Nothing</button>
                        </td>
                        <td class="fields-selector-right">
                            <select name="fields" id="fields" multiple="multiple"/>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
		        <div class="toolbar">
		            <table border="0" cellpadding="0" cellspacing="0" width="100%">
		                <tr>
		                    <td width="100%">
		                    </td>
                            <td><button type="button" onclick="alert('Not implemented yet!')">Export</button></td>
		                    <td><button type="button" onclick="window.close()">Close</button></td>
		                </tr>
		            </table>
		        </div>
            </td>
        </tr>
    </table>

</body>
</html>
