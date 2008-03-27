<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>View Editor</title>
    <script type="text/javascript">
    
        var onSelect = function(){
            onEdit();
        }
        
        var onDelete = function(){
        
            var tree = view_tree;
            var selected = tree.selection[0] || null;
            
            if (!selected) {
                return;
            }
            
            if (!confirm('Do you really want to remove this node?')) {
                return;
            }            
            
            var rinfo = tree.row_info[selected.id];
            var record = rinfo.record;
            var data = record.data;
            
            var req = Ajax.JSON.post('/viewed/save/remove', {view_id: data.view_id, xpath_expr: data.xpath});
            req.addCallback(function(obj){
                
                if (obj.error){
                    return alert(obj.error);
                }
                
                tree.reload();
            });
        }
        
        var onAdd = function(){
        
            var tree = view_tree;
            var selected = tree.selection[0] || null;
            
            if (!selected) {
                return;
            }
            
            var rinfo = tree.row_info[selected.id];
            var record = rinfo.record;
            var data = record.data;
            
            var req = Ajax.post('/viewed/add', {view_id: data.view_id, xpath_expr: data.xpath});
            req.addCallback(function(xmlHttp){
                var el = getElement('view_ed');
                el.innerHTML = xmlHttp.responseText;
            });
        }
        
        var doAdd = function() {
        
            var form = getElement('view_form');
            var params = {};
            
            forEach(form.elements, function(el){
                params[el.name] = el.value;
            });
            
            var req = Ajax.JSON.post('/viewed/save/node', params);
            req.addCallback(function(obj){
                if (obj.error){
                    return alert(obj.error);
                }

                getElement('view_ed').innerHTML = '';
                view_tree.reload();

            });
            
            return false;        
        }
    
        var onEdit = function() {
        
            var tree = view_tree;
            var selected = tree.selection[0] || null;
            
            if (!selected) {
                return;
            }
            
            var rinfo = tree.row_info[selected.id];
            var record = rinfo.record;
            var data = record.data;
            
            var el = getElement('view_ed');
            
            if (!data.editable) {
                el.innerHTML = '';
                return;
            };
            
            var req = Ajax.post('/viewed/edit', {view_id: data.view_id, xpath_expr: data.xpath});
            req.addCallback(function(xmlHttp){
                el.innerHTML = xmlHttp.responseText;
            });
        }
        
        var doEdit = function() {
        
            var form = getElement('view_form');
            var params = {};
            
            forEach(form.elements, function(el){
                
                var val = el.type == 'checkbox' ? el.checked ? 1 : null : el.value;
                                
                if (el.type == 'select-multiple') {
                
                    val = MochiKit.Base.filter(function(o){
                        return o.selected;
                    }, el.options); 
                    
                    val = MochiKit.Base.map(function(o){
                        return o.value;
                    }, val);
                    
                    val = val.join(',');
                }
                
                if (val) {
                    params[el.name] = val;
                }
            });
            
            var req = Ajax.JSON.post('/viewed/save/properties', params);
            req.addCallback(function(obj){
                if (obj.error){
                    alert(obj.error);
                } else {
                    getElement('view_ed').innerHTML = '';
                }
            });
            
            return false;
        }
        
        var onNew = function(){
            alert("Not implemented yet!");
        }
        
        var onClose = function(){
            window.opener.setTimeout("window.location.reload()", 1);
            window.close();
        }
    
    </script>
</head>
<body>
    <table class="view" border="0">
        <tr>
            <td colspan="2">
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/static/images/icon.gif"/>
                        </td>
                        <td width="100%">View Editor ($view_id - $model)</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td id="view_tr" height="500" width="350">
                <div py:content="tree.display()" style="overflow: scroll; width: 100%; height: 100%; border: solid #999999 1px;"/>
            </td>
            <td id="view_ed" valign="top" height="500"></td>
        </tr>
        <tr class="toolbar">
            <td align="right" colspan="2">
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td><button type="button" title="${_('Add a new field')}" onclick="onNew()">New</button></td>
                            <td><button type="button" title="${_('Add a field')}" onclick="onAdd()">Add</button></td>
                            <td><button type="button" title="${_('Delete current field')}" onclick="onDelete()">Delete</button></td>
                            <td><button type="button" title="${_('Edit current field')}" onclick="onEdit()">Edit</button></td>
                            <td width="100%">&nbsp;</td>
                            <td><button type="button" onclick="onClose()">Close</button></td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</body>
</html>
