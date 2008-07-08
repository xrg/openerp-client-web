<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>Manage Views ($model)</title>
    <script type="text/javascript">
    
        function do_select(id, src){
            var radio = MochiKit.DOM.getElement(src + '/' + id);
			if (radio) {
				radio.checked = true;
			}
        }
        
        function doCreate() {
            var vf = document.forms['view_form'];
            vf.submit();
        }
        
        function doCancel() {
            var edt = getElement('view_editor');
            var lst = getElement('view_list');
            
            edt.style.display = "none";
            lst.style.display = "";
        }
        
        function doClose() {
            window.opener.setTimeout("window.location.reload()", 0);
            window.close();
        }
        
        function onNew() {
            var edt = getElement('view_editor');
            var lst = getElement('view_list');
            
            var nm = getElement('name');
            nm.value = getElement('model').value + '.custom_' + Math.round(Math.random() * 1000);
            
            edt.style.display = "";
            lst.style.display = "none";
        }
        
        function onEdit() {
            
            var list = new ListView('_terp_list');
            var boxes = list.getSelectedItems();

            if (boxes.length == 0){
                alert('Please select a view...');
                return;
            }
            
            openWindow(getURL('/viewed', {view_id: boxes[0].value}));
        }
        
        function onRemove() {
        
            var list = new ListView('_terp_list');
            var boxes = list.getSelectedItems();

            if (boxes.length == 0){
                alert('Please select a view...');
                return;
            }
            
            if (!window.confirm('Do you realy want to remove this view?')){
                return;
            }
            
            window.location.href = '/viewlist/delete?model=${model}&amp;id=' + boxes[0].value;
        }
		
        MochiKit.DOM.addLoadEvent(function(evt){
            
            if (!window.opener) 
                return;

            var id = window.opener.document.getElementById('_terp_view_id').value;
            
            if (!MochiKit.DOM.getElement('_terp_list/' + id)) {
                
                var list = new ListView('_terp_list');
                var ids = list.getRecords();

                if (ids.length) {
                    id = ids[0];
                }
            }
            
            do_select(parseInt(id), '_terp_list');
        });		
        
    </script>
</head>
<body>

    <table id="view_list" class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/static/images/icon.gif"/>
                        </td>
                        <td width="100%">Manage Views ($model)</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td py:content="screen.display()">List View</td>
        </tr>
        <tr>
            <td>
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td>
                                <button type="button" onclick="onNew()">New</button>
                                <button type="button" onclick="onEdit()">Edit</button>
                                <button type="button" onclick="onRemove()">Remove</button>
                            </td>
                            <td width="100%"></td>
                            <td>
                                <button type="button" onclick="doClose()">Close</button>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
    
    <table id="view_editor" style="display: none;" class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/static/images/icon.gif"/>
                        </td>
                        <td width="100%">Create a view ($model)</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <form id="view_form" action="/viewlist/create">
                    <input type="hidden" id="model" name="model" value="$model"/>
                    <table width="400" align="center" class="fields">
                        <tr>
                            <td class="label">View Name:</td>
                            <td class="item"><input type="text" id="name" name="name" class="requiredfield"/></td>
                        </tr>
                        <tr>
                            <td class="label">View Type:</td>
                            <td class="item">
                                <select id="type" name="type" class="requiredfield">
                                    <option value="form">Form</option>
                                    <option value="tree">Tree</option>
                                    <option value="graph">Graph</option>
                                    <option value="calendar">Calendar</option>
                                </select>
                            </td>
                        </tr>
                        <tr>
                            <td class="label">Priority:</td>
                            <td class="item"><input type="text" id="priority" name="priority" value="16" class="requiredfield"/></td>
                        </tr>
                    </table>
                </form>
            </td>
        </tr>
        <tr>
            <td>
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td width="100%"></td>
                            <td>
                                <button type="button" onclick="doCreate()">Save</button>
                                <button type="button" onclick="doCancel()">Cancel</button>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>

</body>
</html>
